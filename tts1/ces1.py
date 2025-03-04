import logging
from openai import OpenAI
import json
import httpx

api_key = 'geekaiapp'  # 替换为你的实际 API key
base_url = 'https://green-dawn-c018.liangxiaogeek6.workers.dev/v1/' # 替换为你的自定义域，默认加 /v1


client = OpenAI(
    api_key=api_key,
    base_url=base_url
)



data = {
    'model': 'tts-1',
    'input': '你好啊，亲爱的朋友们',
    'voice': 'zh-CN-YunjianNeural',
    'response_format': 'mp3',
    'speed': 1.0,
}


try:
    response = client.audio.speech.create(
       **data
    )
    with open('./test_openai.mp3', 'wb') as f:
        f.write(response.content)
    print("MP3 file saved successfully to test_openai.mp3")

except Exception as e:
    print(f"An error occurred: {e}")
