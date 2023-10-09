from transformers import AutoTokenizer, LlamaForCausalLM

model = LlamaForCausalLM.from_pretrained("blockplacer4/Hobby-Ki-V2")
tokenizer = AutoTokenizer.from_pretrained("blockplacer4/Hobby-Ki-V2")

prompt = "Was ist das Beste hobby?"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids, max_length=30)
tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
