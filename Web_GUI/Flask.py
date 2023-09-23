from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from googletrans import Translator

app = Flask(__name__)
def translate(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

model_name = "gpt2" 
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']
    bot_response = chat_with_ai(user_message)
    return jsonify({'bot_response': bot_response})

def chat_with_ai(user_message):
    user_message_trans = translate(user_message, "en")
    input_ids = tokenizer.encode("User: " + user_message_trans, return_tensors="pt")
    chat_output = model.generate(input_ids, max_length=10000, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50, top_p=0.95)
    bot_response = tokenizer.decode(chat_output[0], skip_special_tokens=True)
    bot_response_trans = translate(bot_response, "de")
    return bot_response_trans

if __name__ == '__main__':
    app.run(debug=True)