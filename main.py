from settings import API_KEY, PROXY
import asyncio
import aiohttp


async def question_for_gpt(messages: list) -> list:
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

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, proxy=PROXY, json=data) as response:
            if response.status == 200:
                response_data = await response.json()
                answer = response_data['choices'][0]['message']['content']
                model = response_data['model']
                tokens_info = str(response_data['usage'])
                print(f'{model} Ответил на ваш запрос: {answer}\n{tokens_info}')
                print(type(response_data))
                print(response_data)
    return answer


if __name__ == "__main__":
    messages = []
    messages.append({'role': 'user', 'content': 'Привет'})
    # task = asyncio.create_task(question_for_gpt(messages))
    asyncio.run(question_for_gpt(messages))
    # asyncio.gather(task)
    messages.append({'role': 'assistant', 'content': question_for_gpt(messages)})
