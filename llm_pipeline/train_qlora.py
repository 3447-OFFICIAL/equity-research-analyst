"""
QLoRA fine-tuning script for Llama-3-8B-Instruct using HuggingFace PEFT and TRL.
This script is designed to run on a single consumer GPU (e.g. RTX 4090) or AWS G5 instance.
"""
# Note: Requires `pip install transformers trl peft bitsandbytes datasets`

import os
# from datasets import load_dataset
# from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
# from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
# from trl import SFTTrainer

def train():
    print("Initializing QLoRA Fine-tuning pipeline for Financial Research LLM...")
    
    # 1. Configuration
    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    dataset_path = "dataset.jsonl"
    output_dir = "./finance-llama3-8b-lora"
    
    # bnb_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_quant_type="nf4",
    #     bnb_4bit_compute_dtype=torch.float16
    # )
    
    # 2. Load Model
    # model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, device_map="auto")
    # model = prepare_model_for_kbit_training(model)
    
    # 3. LoRA Configuration
    # lora_config = LoraConfig(
    #     r=16, 
    #     lora_alpha=32, 
    #     target_modules=["q_proj", "k_proj", "v_proj", "o_proj"], 
    #     lora_dropout=0.05, 
    #     bias="none", 
    #     task_type="CAUSAL_LM"
    # )
    # model = get_peft_model(model, lora_config)
    
    # 4. Train
    # trainer = SFTTrainer(
    #     model=model,
    #     train_dataset=dataset,
    #     peft_config=lora_config,
    #     dataset_text_field="text",
    #     max_seq_length=4096,
    #     args=TrainingArguments(
    #         output_dir=output_dir,
    #         per_device_train_batch_size=2,
    #         gradient_accumulation_steps=4,
    #         learning_rate=2e-4,
    #         num_train_epochs=3,
    #     )
    # )
    # trainer.train()
    # trainer.model.save_pretrained(output_dir)
    print(f"Training completed. Adapter saved to {output_dir}")

if __name__ == "__main__":
    train()
