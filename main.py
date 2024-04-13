import requests
from settings import API_KEY, PROXIES


def question_for_gpt(messages: list) -> list:
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        'model': 'gpt-3.5-turbo',
        "messages": messages,
        'temperature': 0.7
        }

    response = requests.post(url, headers=headers, json=data, proxies=PROXIES)

    if response.status_code == 200:
        response_data = response.json()
        model = response_data['model']
        answer = response_data['choices'][0]['message']['content']
        tokens_info = str(response_data['usage'])
        print(f'{model} Ответил на ваш запрос: {answer}\n{tokens_info}')
        return answer
    else:
        return 0


if __name__ == "__main__":
    messages = []
    while True:
        messages.append({'role': 'user', 'content': input()})
        messages.append({'role': 'assistant', 'content': question_for_gpt(messages)})

    # qwery_1 = 'У Миши 10 яблок. 4 яблока он решил раздать Кате и Марине, поровну. Сколько яблок будет у Марины?'
    # qwery_2 = 'Сколько яблок останется у Миши?'
    # question_for_gpt("Кому Миша отдал свои яблоки?")