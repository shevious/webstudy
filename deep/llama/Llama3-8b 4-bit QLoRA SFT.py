import os
import copy
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import numpy as np
from datasets import Dataset
from scipy.special import softmax
from sklearn.preprocessing import LabelEncoder
from transformers import (
    BitsAndBytesConfig,
    LlamaPreTrainedModel,
    LlamaModel,
    AutoTokenizer,
    PreTrainedTokenizerBase, 
    EvalPrediction,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
)
from transformers.modeling_outputs import CausalLMOutputWithPast
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from sklearn.metrics import log_loss, accuracy_score
from trl import ModelConfig, SFTTrainer, get_kbit_device_map, get_peft_config, get_quantization_config

from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

from accelerate import PartialState

device_map="DDP" # for DDP and running with `accelerate launch test_sft.py`
#device_map='auto' # for PP and running with `python test_sft.py`

if device_map == "DDP":
    device_string = PartialState().process_index
    device_map={'':device_string}

TRAIN_CSV = "lmsys-chatbot-arena/train.csv"
model_path = "unsloth/llama-3-8b-Instruct-bnb-4bit"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MAX_LENGTH = 1024
target_columns = ['winner_model_a', 'winner_model_b', 'winner_tie']
columns_to_vectorize = ["prompt", "response_a", "response_b"]

train = pd.read_csv(TRAIN_CSV)
train = train.head(100)
train['label'] = train[target_columns].idxmax(axis=1) 
label_encoder = LabelEncoder()
train['label'] = label_encoder.fit_transform(train['label'])
train = train[columns_to_vectorize + ['label']]

import json
def filter(s):
    #print(s)
    arr = eval(s, {"null": ""})
    arr_ret = []
    for s2 in arr:
        s3 = s2.encode('utf-8', errors='replace').decode()
        arr_ret.append(json.dumps(s3))
    s_ret =  '['+','.join(arr_ret)+']'
    #if s != s_ret:
        #print('###')
        #print(s)
        #print(s_ret)
    return s_ret

for i, row in train.iterrows():
    #s = row['prompt']
    #s = row['response_a']
    #print(filter(s))
    train.loc[i, 'prompt'] = filter(row['prompt'])
    train.loc[i, 'response_a'] = filter(row['response_a'])
    train.loc[i, 'response_b'] = filter(row['response_b'])
    #print(train)


tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.add_eos_token = True
tokenizer.padding_side = 'right'

LABEL_IDS = [tokenizer(i, add_special_tokens=False)["input_ids"][0] for i in ['a', 'b', 'tie']]

def tokenize(example, tokenizer):
    prompt = tokenizer('<prompt>: ' + " ".join(eval(example['prompt'], {"null": ""})), add_special_tokens=False)["input_ids"]
    #if example['response_a'].startswith('["The question of whether it is'):
        #print('#### check')
        #example['response_a'] = '["The question of whether it is morally"]'
    response_a = tokenizer('\n\n<response_a>: ' + " ".join(eval(example['response_a'], {"null": ""})), add_special_tokens=False)["input_ids"]
    response_b = tokenizer('\n\n<response_b>: ' + " ".join(eval(example['response_b'], {"null": ""})), add_special_tokens=False)["input_ids"]
    if len(prompt+response_a+response_b) > MAX_LENGTH:
        prompt = tokenizer('<prompt>: ' + eval(example['prompt'], {"null": ""})[-1], add_special_tokens=False)["input_ids"][:256]
        response_a = tokenizer('\n\n<response_a>: ' + eval(example['response_a'], {"null": ""})[-1], add_special_tokens=False)["input_ids"][:512]
        response_b = tokenizer('\n\n<response_b>: ' + eval(example['response_b'], {"null": ""})[-1], add_special_tokens=False)["input_ids"][:512]
    extra_prompt = tokenizer('\n\n---------\nWhich is the better response for the prompt ? a or b or tie ?\n\nAnswer: ', add_special_tokens=False)["input_ids"]

    label_token_id = LABEL_IDS[int(example['label'])]
    input_ids = [tokenizer.bos_token_id] + prompt + response_a + response_b + extra_prompt + [label_token_id] + [tokenizer.eos_token_id]
    attention_mask = len(input_ids)*[1]
    labels = [-100]* len([tokenizer.bos_token_id] + prompt + response_a + response_b + extra_prompt) + [label_token_id] + [tokenizer.eos_token_id]
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels
    }


def load_data(df, tokenizer):
    raw_datasets = Dataset.from_pandas(df)
    #print(raw_datasets)
    #print(raw_datasets.column_names)
    tokenized_datasets = raw_datasets.map(
        tokenize, 
        remove_columns=raw_datasets.column_names,
        fn_kwargs={'tokenizer': tokenizer}
    )
    return tokenized_datasets

def compute_metrics(pred):
    logits, labels = pred
    preds = logits.argmax(axis=-1)
    label_tokens_ids = np.array(LABEL_IDS)
    index_mapping = {value.item(): idx for idx, value in enumerate(label_tokens_ids)}
    labels = labels[np.isin(labels, label_tokens_ids)]
    labels = np.array([index_mapping[label.item()] for label in labels])
    acc = accuracy_score(labels, preds)
    probs = softmax(logits, axis=-1)
    log_loss_ = log_loss(labels, probs)
    return {'accuracy': acc, 'log_loss': log_loss_}

n_splits = 5
fold_idx = 0
ds = load_data(train, tokenizer)
folds = [
    (
        [i for i in range(len(ds)) if i % n_splits != fold_idx],
        [i for i in range(len(ds)) if i % n_splits == fold_idx]
    ) 
    for fold_idx in range(n_splits)
]
train_idx, eval_idx = folds[fold_idx]


class Llama3ForSFT(LlamaPreTrainedModel):
    _tied_weights_keys = ["lm_head.weight"]
    def __init__(self, config):
        super().__init__(config)
        self.model = LlamaModel(config)
        self.vocab_size = config.vocab_size
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        self.post_init()

    def forward(
        self,
        input_ids= None,
        attention_mask= None,
        position_ids = None,
        past_key_values= None,
        inputs_embeds= None,
        labels= None,
        use_cache= None,
        output_attentions= None,
        output_hidden_states = None,
        return_dict= None,
        cache_position = None,
    ):
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            cache_position=cache_position,
        )
        hidden_states = outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.lm_head.weight.split(self.vocab_size // self.config.pretraining_tp, dim=0)
            logits = [F.linear(hidden_states, lm_head_slices[i]) for i in range(self.config.pretraining_tp)]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.lm_head(hidden_states)
        logits = logits.float()

        loss = None
        if labels is not None:
            # Shift so that tokens < n predict n
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            # Flatten the tokens
            loss_fct = nn.CrossEntropyLoss()
            shift_logits = shift_logits.view(-1, self.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            # Enable model parallelism
            shift_labels = shift_labels.to(shift_logits.device)

            label_tokens_ids = torch.tensor(LABEL_IDS,device=shift_labels.device)
            index_mapping = {value.item(): idx for idx, value in enumerate(label_tokens_ids)}
            true_labels = shift_labels[torch.isin(shift_labels, label_tokens_ids)]
            true_labels = torch.tensor([index_mapping[label.item()] for label in true_labels], device=true_labels.device)
            true_logits = shift_logits[torch.isin(shift_labels, label_tokens_ids)][:,label_tokens_ids]
            loss = loss_fct(true_logits, true_labels)

        return CausalLMOutputWithPast(
            loss=loss,
            logits=true_logits,
        )
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias='none',
    inference_mode=False,
    task_type=TaskType.CAUSAL_LM,
    target_modules=['q_proj', 'k_proj', 'v_proj',], 
)

model = Llama3ForSFT.from_pretrained(
    model_path, 
    torch_dtype=torch.float16, 
    device_map = device_map,
    #device_map = get_kbit_device_map(),
    #quantization_config = bnb_config,
)
model.config.use_cache = False
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)
print(model)
#model.print_trainable_parameters()

args = TrainingArguments(
    output_dir='output',
    overwrite_output_dir = True,
    evaluation_strategy = "epoch",
    save_strategy = "steps",
    save_steps=200,
    save_total_limit=1,
    logging_strategy="steps",
    logging_steps=10,
    warmup_steps=20,
    optim="adamw_8bit",
    learning_rate=2e-4,
    #per_device_train_batch_size=2,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=2,
    num_train_epochs=1,
    fp16=True,
    metric_for_best_model="log_loss",
    greater_is_better = False,
    gradient_checkpointing = True,
    gradient_checkpointing_kwargs = {"use_reentrant": False}, #must be false for DDP
    report_to="none",
)

trainer = Trainer(
    args=args,
    model=model,
    train_dataset=ds.select(train_idx),
    eval_dataset=ds.select(eval_idx),
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer),
    compute_metrics=compute_metrics,
    #peft_config = peft_config,
)
trainer.train()



