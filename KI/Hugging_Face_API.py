from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


# Hugging Face API-Konfiguration
HF_API_URL = "https://api-inference.huggingface.co/models/blockplacer4/Hobby-Ki-V6"
HF_API_HEADERS = {"Authorization": "Bearer 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"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']

    # Anfrage an Hugging Face API senden
    hf_api_payload = {"inputs": user_message}
    hf_response = requests.post(HF_API_URL, headers=HF_API_HEADERS, json=hf_api_payload)
    
    if hf_response.status_code == 200:
        bot_response = hf_response.json()
        Bot = bot_response[0]['generated_text'].split('\n', 1)[1]
        
        return jsonify({'bot_response': Bot})
    else:
        return jsonify({'bot_response': 'Fehler bei der Anfrage an die Hugging Face API'})

if __name__ == '__main__':
    app.run(debug=True)
