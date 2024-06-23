import json
import requests
from config import GPT_KEY

def send_prompt(text):
    pre_input = 'O comentário abaixo foi realizado por um usuário do youtube: " '
    pos_input = ' ". Dentre os 4 tipos de sentimento abaixo: positivo, negativo, neutro e indefinido, qual você acha que melhor representa o comentário? Ps: Responda apenas com 1 palavra'

    headers = {
        'Authorization': 'Bearer ' + GPT_KEY,
        'Content-Type': 'application/json',
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": pre_input + json.dumps(text) + pos_input
            }
        ]
    }

    url = 'https://api.openai.com/v1/chat/completions'

    response = requests.post(url, headers=headers, data=json.dumps(data))

    data_response = response.json()
    sentiment = data_response['choices'][0]['message']['content']

    return sentiment

def evaluate_sentiment(json_file):
    with open(json_file, 'r') as file:
        json_data = file.read()
    list = json.loads(json_data)
    print(list)
    response = []
    for item in list:
        if 'text' in item:
            text = item['text']
            sentiment = send_prompt(text)
            response.append(sentiment)
    return response