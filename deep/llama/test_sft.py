# Script from: https://github.com/huggingface/trl/issues/1303
# Run this with DDP with "accelerate launch test_sft.py"
from datasets import load_dataset
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoTokenizer
from peft import LoraConfig
from trl import SFTTrainer
from transformers import TrainingArguments
from accelerate import PartialState

device_map="DDP" # for DDP and running with `accelerate launch test_sft.py`
# device_map='auto' # for PP and running with `python test_sft.py`

if device_map == "DDP":
    device_string = PartialState().process_index
    device_map={'':device_string}

# Load the dataset
dataset_name = "timdettmers/openassistant-guanaco"
dataset = load_dataset(dataset_name, split="train")

# Load the model + tokenizer
model_name = "meta-llama/Llama-2-7b-hf"

import os
max_seq_length = 512
token = os.environ['HF_ACCESS_TOKEN']
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=token, max_seq_length=max_seq_length)
tokenizer.pad_token = tokenizer.eos_token
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    trust_remote_code=True,
    use_cache = False,
    device_map = device_map,
    token = token,
)

# PEFT config
lora_alpha = 8
lora_dropout = 0.1
lora_r = 32
peft_config = LoraConfig(
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    r=lora_r,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["k_proj", "q_proj", "v_proj", "up_proj", "down_proj", "gate_proj"],
    modules_to_save=["embed_tokens", "input_layernorm", "post_attention_layernorm", "norm"],
)

# Args 
max_seq_length = 512
output_dir = "./results"
per_device_train_batch_size = 8
gradient_accumulation_steps = 2
optim = "adamw_torch"
save_steps = 10
logging_steps = 1
learning_rate = 2e-4
max_grad_norm = 0.3
max_steps = 1 # Approx the size of guanaco at bs 8, ga 2, 2 GPUs. 
warmup_ratio = 0.1
lr_scheduler_type = "cosine"
training_arguments = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=per_device_train_batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    optim=optim,
    save_steps=save_steps,
    logging_steps=logging_steps,
    learning_rate=learning_rate,
    fp16=True,
    max_grad_norm=max_grad_norm,
    max_steps=max_steps,
    warmup_ratio=warmup_ratio,
    group_by_length=True,
    lr_scheduler_type=lr_scheduler_type,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs = {"use_reentrant": False}, #must be false for DDP
    #report_to="wandb",
)

# Trainer 
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    #dataset_text_field="text",
    tokenizer=tokenizer,
    args=training_arguments,
    #max_seq_length=max_seq_length,
)

# Train :)
trainer.train()
