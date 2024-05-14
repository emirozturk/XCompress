import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)
from util import (
    bin_usc,
    count_unique_symbols,
    round_to_class,
    get_file_size
)

def detect_algorithm(filename,mode):
    base_model_name = "Llama-2-7b-hf/checkpoint-2000"
    model = AutoModelForCausalLM.from_pretrained(base_model_name)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name,padding_side = 'right')
    tokenizer.pad_token = tokenizer.eos_token
    
    usc = bin_usc(count_unique_symbols(filename))
    file_size = round_to_class(get_file_size)
    eval_prompt = f"### Instruction: We need to find algorithm from given input params: (usc:{usc}, file_size:{file_size}, compression_type: {mode})."
    model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")

    model.eval()
    with torch.no_grad():
        result = tokenizer.decode(model.generate(**model_input, max_new_tokens=150, repetition_penalty=1.15)[0], skip_special_tokens=True)
    algorithm = result.split("The algorithm is: ")[1].strip().replace(".", "")
    return algorithm