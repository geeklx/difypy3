import requests
from fastapi import FastAPI, HTTPException

api_url = "https://api.imgrender.cn/open/v1/pics"
auth_token = "geekapp"

# 公共header
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}

# 示例参数
params = {
    "x": 248,
    "y": 25,
    "width": 120,
    "height": 120,
    "url": "https://img-chengxiaoli-1253325493.cos.ap-beijing.myqcloud.com/bikers_327390-13.jpg",
    "borderRadius": 60,
    "zIndex": 1
}

app = FastAPI()


@app.post("/generate-audio/")
async def post2imgrender1(params):
    # audiourl=api_url+"/audio/speech"
    audiourl = api_url
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    data = params
    response = requests.post(audiourl, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        url = result.get('url')  # 假设返回的 JSON 中包含 'url' 字段
        return {
            "url": url
        }
    else:
        raise HTTPException(status_code=response.status_code, detail="请求失败")


import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8087)
