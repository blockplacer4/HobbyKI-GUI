from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import os
import replicate

app = Flask(__name__)


def translate(text):
    translated = GoogleTranslator(source='auto', target='de').translate(text=text)
    return translated


os.environ["REPLICATE_API_TOKEN"] = "r8_ELYcYXUjWpfDkGwboON58eCsBhK3p9x35KZ2U"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']
    bot_response = chat_with_ai(user_message)
    resp = translate(bot_response)
    return jsonify({'bot_response': resp})


def chat_with_ai(user_message):
    return "Heyo"
    # Secret Connection with Secret API Server <3


if __name__ == '__main__':
    app.run(debug=True)
