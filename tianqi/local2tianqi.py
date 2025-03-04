from fastapi import FastAPI, Request, HTTPException
import random

app = FastAPI()

@app.post('/weather')
async def get_weather(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header != 'Bearer geekapp':
        raise HTTPException(status_code=403, detail="Invalid Authorization header")
    request_data = await request.json()
    city = request_data.get('city', None)
    if city is None:
        return {
            'status': 'error',
            'errorInfo': 'No city provided',
            'data': None
        }

    # 随机生成温度，风速和风向
    temperature = f'{random.randint(10, 20)}'
    windspeed = f'{random.randint(1, 5)}级'
    winddirect = random.choice(['北风', '南风', '西风', '东风'])  # 随机选择风向
    # 返回对LLM友好的字符串格式的响应
    return f"{city}今天是晴天，温度{temperature}, 风速{windspeed}, 风向{winddirect}"

import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8087)