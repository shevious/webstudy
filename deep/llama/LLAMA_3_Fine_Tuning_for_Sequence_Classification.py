#!/usr/bin/env python
# coding: utf-8


device_map="DDP" # for DDP and running with `accelerate launch test_sft.py`
#device_map='auto' # for PP and running with `python test_sft.py`

from accelerate import PartialState

if device_map == "DDP":
    from accelerate import Accelerator
    accelerator = Accelerator()

    device_string = PartialState().process_index
    device_map={'':device_string}

import os
import random
import functools
import csv
import pandas as pd
import numpy as np
import torch
import torch.nn.functional as F
import evaluate

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, confusion_matrix, classification_report, balanced_accuracy_score, accuracy_score

from scipy.stats import pearsonr
from datasets import Dataset, DatasetDict
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)

from pathlib import Path
path = Path('us-patent-phrase-to-phrase-matching')

iskaggle = False

if not iskaggle and not path.exists():
    import zipfile,kaggle
    kaggle.api.competition_download_cli(str(path))
    zipfile.ZipFile(f'{path}.zip').extractall(path)


from pathlib import Path
path = Path('us-patent-phrase-to-phrase-matching')

df = pd.read_csv(path/'train.csv')

df['score_ascat']=df['score'].astype('category')
df['score_category']=df['score_ascat'].cat.codes

print(df)

df['score_ascat'].cat.categories
df.describe(include='object')


category_map = {code: category for code, category in enumerate(df['score_ascat'].cat.categories)}
print(category_map)


# ### Convert from Pandas DataFrame to Hugging Face Dataset
# * Also let's shuffle the training set.
# * We put the components train,val,test into a DatasetDict so we can access them later with HF trainer.
# * Later we will add a tokenized dataset
# 

df_test = pd.read_csv(path/'test.csv')

train_size = 0.8 # 80% of data
test_size = 0.2 # 20% of data
df_train, df_val = train_test_split(pd.read_csv(path/'train.csv'), train_size=train_size, test_size=test_size, random_state=42)

def generate_features(df):
  df['input'] = 'TEXT1: ' + df.context + '; TEXT2: ' + df.target + '; ANC1: ' + df.anchor
  if 'score' in df.columns:
    df['score_ascat']=df['score'].astype('category')
    df['score_category']=df['score_ascat'].cat.codes
  else:
    df['score_category'] = pd.NA

generate_features(df_train)
generate_features(df_val)


# Converting pandas DataFrames into Hugging Face Dataset objects:
dataset_train = Dataset.from_pandas(df_train.drop(['score_ascat', 'score'],axis=1).reset_index(drop=True))
dataset_val = Dataset.from_pandas(df_val.drop(['score_ascat', 'score'],axis=1).reset_index(drop=True))


# Combine them into a single DatasetDict
dataset = DatasetDict({
    'train': dataset_train,
    'val': dataset_val,
})
print(dataset)


# * Since our classes are not balanced let's calculate class weights based on inverse value counts
# * Convert to pytorch tensor since we will need it


df_train.score_category.value_counts(normalize=True)


class_weights=(1/df_train.score_category.value_counts(normalize=True).sort_index()).tolist()
class_weights=torch.tensor(class_weights)
class_weights=class_weights/class_weights.sum()
class_weights


# ## Load LLama model with 4 bit quantization as specified in bits and bytes and prepare model for peft training
# 
# ### Model Name

model_name = "meta-llama/Meta-Llama-3-8B"

# #### Quantization Config (for QLORA)

quantization_config = BitsAndBytesConfig(
    load_in_4bit = True, # enable 4-bit quantization
    bnb_4bit_quant_type = 'nf4', # information theoretically optimal dtype for normally distributed weights
    bnb_4bit_use_double_quant = True, # quantize quantized weights //insert xzibit meme
    bnb_4bit_compute_dtype = torch.bfloat16 # optimized fp format for ML
)

# #### Lora Config

lora_config = LoraConfig(
    r = 16, # the dimension of the low-rank matrices
    lora_alpha = 8, # scaling factor for LoRA activations vs pre-trained weight activations
    target_modules = ['q_proj', 'k_proj', 'v_proj', 'o_proj'],
    lora_dropout = 0.05, # dropout probability of the LoRA layers
    bias = 'none', # wether to train bias weights, set to 'none' for attention layers
    task_type = 'SEQ_CLS'
)

# #### Load model
# * AutomodelForSequenceClassification
# * Num Labels is # of classes
# 

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    num_labels=len(category_map),
    device_map=device_map,
)

print(model)

# * prepare_model_for_kbit_training() function to preprocess the quantized model for training.

model = prepare_model_for_kbit_training(model)
print(model)


# * get_peft_model prepares a model for training with a PEFT method such as LoRA by wrapping the base model and PEFT configuration with get_peft_model

model = get_peft_model(model, lora_config)
print(model)

# ### Load the tokenizer
# 
# #### Since LLAMA3 pre-training doesn't have EOS token
# * Set the pad_token_id to eos_token_id
# * Set pad token ot eos_token

tokenizer = AutoTokenizer.from_pretrained(model_name, add_prefix_space=True)

tokenizer.pad_token_id = tokenizer.eos_token_id
tokenizer.pad_token = tokenizer.eos_token

# #### Update some model configs
# * Must use .cache = False as below or it crashes from my experience

model.config.pad_token_id = tokenizer.pad_token_id
model.config.use_cache = False
model.config.pretraining_tp = 1


# # Trainer Components
# * model
# * tokenizer
# * training arguments
# * train dataset
# * eval dataset
# * Data Collater
# * Compute Metrics
# * class_weights: In our case since we are using a custom trainer so we can use a weighted loss we will subclass trainer and define the custom loss.

# #### Create LLAMA tokenized dataset which will house our train/val parts during the training process but after applying tokenization

MAX_LEN = 512
col_to_delete = ['id', 'anchor', 'context', 'target']

def llama_preprocessing_function(examples):
    return tokenizer(examples['input'], truncation=True, max_length=MAX_LEN)

tokenized_datasets = dataset.map(llama_preprocessing_function, batched=True, remove_columns=col_to_delete)
tokenized_datasets = tokenized_datasets.rename_column("score_category", "label")
tokenized_datasets.set_format("torch")


# ## Data Collator
# A **data collator** prepares batches of data for training or inference in machine learning, ensuring uniform formatting and adherence to model input requirements. This is especially crucial for variable-sized inputs like text sequences.
# 
# ### Functions of Data Collator
# 
# 1. **Padding:** Uniformly pads sequences to the length of the longest sequence using a special token, allowing simultaneous batch processing.
# 2. **Batching:** Groups individual data points into batches for efficient processing.
# 3. **Handling Special Tokens:** Adds necessary special tokens to sequences.
# 4. **Converting to Tensor:** Transforms data into tensors, the required format for machine learning frameworks.
# 
# ### `DataCollatorWithPadding`
# 
# The `DataCollatorWithPadding` specifically manages padding, using a tokenizer to ensure that all sequences are padded to the same length for consistent model input.
# 
# - **Syntax:** `collate_fn = DataCollatorWithPadding(tokenizer=tokenizer)`
# - **Purpose:** Automatically pads text data to the longest sequence in a batch, crucial for models like BERT or GPT.
# - **Tokenizer:** Uses the provided `tokenizer` for sequence processing, respecting model-specific vocabulary and formatting rules.
# 
# This collator is commonly used with libraries like Hugging Face's Transformers, facilitating data preprocessing for various NLP models.
# 

collate_fn = DataCollatorWithPadding(tokenizer=tokenizer)


# # define which metrics to compute for evaluation
# * We will use balanced accuracy and accuracy for simplicity

def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    try:
        # it's a classification task, take the argmax
        predictions_processed = np.argmax(predictions, axis=1)

        # Calculate Pearson correlation
        pearson, _ = pearsonr(predictions_processed, labels)

        return {'pearson': pearson}
    except Exception as e:
        print(f"Error in compute_metrics: {e}")
        return {'pearson': None}


# ### Define custom trainer with classweights
# * We will have a custom loss function that deals with the class weights and have class weights as additional argument in constructor

class CustomTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure label_weights is a tensor
        if class_weights is not None:
            self.class_weights = torch.tensor(class_weights, dtype=torch.float32).to(self.args.device)
        else:
            self.class_weights = None

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        # Extract labels and convert them to long type for cross_entropy
        labels = inputs.pop("labels").long()

        # Forward pass
        outputs = model(**inputs)

        # Extract logits assuming they are directly outputted by the model
        logits = outputs.get('logits')

        # Compute custom loss with class weights for imbalanced data handling
        if self.class_weights is not None:
            loss = F.cross_entropy(logits, labels, weight=self.class_weights)
        else:
            loss = F.cross_entropy(logits, labels)

        return (loss, outputs) if return_outputs else loss

# # define training args

training_args = TrainingArguments(
    output_dir = 'sequence_classification',
    learning_rate = 1e-4,
    per_device_train_batch_size = 8,
    per_device_eval_batch_size = 8,
    num_train_epochs = 2,
    weight_decay = 0.01,
    evaluation_strategy = 'epoch',
    save_strategy = 'epoch',
    load_best_model_at_end = True,
    ddp_find_unused_parameters=False,
    #gradient_checkpointing = False,
    #gradient_checkpointing_kwargs = {"use_reentrant": True}, #must be false for DDP
)

# #### Define custom trainer

trainer = CustomTrainer(
    model = model,
    args = training_args,
    train_dataset = tokenized_datasets['train'],
    eval_dataset = tokenized_datasets['val'],
    tokenizer = tokenizer,
    data_collator = collate_fn,
    compute_metrics = compute_metrics,
    class_weights=class_weights,
)

# * https://huggingface.co/docs/transformers/en/training

# ### Run trainer!

train_result = trainer.train()


# #### Let's check the results
# * I wrapped in a function a convenient way add the predictions

def make_predictions(model, df):
  # Convert summaries to a list
  sentences = df.input.tolist()

  # Define the batch size
  batch_size = 32  # You can adjust this based on your system's memory capacity

  # Initialize an empty list to store the model outputs
  all_outputs = []

  # Process the sentences in batches
  for i in range(0, len(sentences), batch_size):
      # Get the batch of sentences
      batch_sentences = sentences[i:i + batch_size]

      # Tokenize the batch
      inputs = tokenizer(batch_sentences, return_tensors="pt", padding=True, truncation=True, max_length=512)

      # Move tensors to the device where the model is (e.g., GPU or CPU)
      inputs = {k: v.to('cuda' if torch.cuda.is_available() else 'cpu') for k, v in inputs.items()}

      # Perform inference and store the logits
      with torch.no_grad():
          outputs = model(**inputs)
          all_outputs.append(outputs['logits'])

  final_outputs = torch.cat(all_outputs, dim=0)
  df['predictions']=final_outputs.argmax(axis=1).cpu().numpy()
  df['predictions']=df['predictions'].apply(lambda l:category_map[l])

def get_performance_metrics(df_test):
  y_test = df_test.score.round()
  y_pred = df_test.predictions.round()
  print(f"comparing test {y_test} and pred {y_pred}")

  print("Confusion Matrix:")
  print(confusion_matrix(y_test, y_pred))

  print("\nClassification Report:")
  print(classification_report(y_test, y_pred))

  print("Balanced Accuracy Score:", balanced_accuracy_score(y_test, y_pred))
  print("Accuracy Score:", accuracy_score(y_test, y_pred))

if accelerator.is_local_main_process:
    make_predictions(model,df_val)

    get_performance_metrics(df_val)
    print(df_val)

    metrics = train_result.metrics
    max_train_samples = len(dataset_train)
    metrics["train_samples"] = min(max_train_samples, len(dataset_train))
    trainer.log_metrics("train", metrics)
    trainer.save_metrics("train", metrics)
    trainer.save_state()

    trainer.save_model("saved_model")
