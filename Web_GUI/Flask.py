from flask import Flask, render_template, request, jsonify
from translate import Translator
import os
import replicate

app = Flask(__name__)


def translate_text(texts):
    translator = Translator(to_lang="de")
    translation = translator.translate(texts)
    return translation.text


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']
    bot_response = chat_with_ai(user_message)
    translated = translate_text(bot_response)
    print(translated)
    print()
    print(bot_response)
    return jsonify({'bot_response': translated})


def chat_with_ai(user_message):
    return "troll"


if __name__ == '__main__':
    app.run(debug=True)
