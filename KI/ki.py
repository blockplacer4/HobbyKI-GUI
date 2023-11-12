import requests
import json

API_URL = "https://api-inference.huggingface.co/models/blockplacer4/Hobby-Ki-V10"
headers = {"Authorization": "Bearer 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"}
prompt_input = "Was ist ein gutes Hobby?"

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({"inputs": "Ich mag Pizza"})

print(output)