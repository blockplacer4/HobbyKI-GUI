from flask import Flask, render_template, request, jsonify
from translate import Translator
import os
import replicate

app = Flask(__name__)


def translate_text(texts):
    translator = Translator(to_lang="de")
    translation = translator.translate(texts)
    return translation.text


os.environ["REPLICATE_API_TOKEN"] = "r8_ELYcYXUjWpfDkGwboON58eCsBhK3p9x35KZ2U"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']
    bot_response = chat_second_ai(user_message)
    translated = translate_text(bot_response)
    print(translated)
    print()
    print(bot_response)
    return jsonify({'bot_response': translated})


def chat_with_ai(user_message):
    resp = ""
    for event in replicate.stream(
            "meta/llama-2-7b-chat",
            input={"prompt": "bitte antworte in 3 **kurzen** Sätzen: " + user_message,
                   "system_prompt": "Du bist ein hilfreicher Assistent, der konsequent die Vorteile des Programmierens als Hobby betont und immer in drei kurzen Sätzen antwortet. Dabei sorgst du stets für eine reibungslose Überleitung zum Thema 'Programmieren als Hobby'. Deine Antworten erfolgen immer auf Deutsch! Du antwortest immer in 3 kurzen Sätzen!",
                   "max_new_tokens": 7},
    ):
        resp += str(event)
    return resp


def chat_second_ai(user_message):
    output = replicate.run(
        "meta/llama-2-7b-chat",
        input={"prompt": user_message + " Bitte Anworte auf Deutsch!",
               "system_prompt": "Du bist ein hilfreicher Assistent, der konsequent die Vorteile des Programmierens als Hobby betont und immer auf Deutsch antwortet. Dabei sorgst du stets für eine reibungslose Überleitung zum Thema 'Programmieren als Hobby'. Deine Antworten erfolgen immer auf Deutsch! Du antwortest immer in 3 kurzen Sätzen!",
               "max_new_tokens": 800})
    string_list = [str(item) for item in output]
    return ''.join(string_list)


if __name__ == '__main__':
    app.run(debug=True)
