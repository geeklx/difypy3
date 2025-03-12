import datetime
import json
import logging
import os
import random
import time
from pathlib import Path

import requests
from fastapi import HTTPException
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# openai_api_key='zhouhuizhou'
openai_api_key1 = 'geekaiapp'
# openai_base_url='https://edgettsapi.duckcloud.fun/v1'
openai_base_url1 = 'https://edge-tts.g1cloudflare.workers.dev/v1'

current_directory = Path.cwd()
path = current_directory / "tmp"
print("完整路径:", path)
output_path1 = path
# output_path1 = 'D:\tmp'
port1 = 5037
ip1 = '127.0.0.1'

region1 = 'ap-nanjing'
secret_id1 = 'x'
secret_key1 = 'x'
bucket1 = 'x'

audiomodel = 'FunAudioLLM/CosyVoice2-0.5B'
voice = 'FunAudioLLM/CosyVoice2-0.5B:david'
videomodel = 'Lightricks/LTX-Video'

siliconflow_api_url = 'https://api.siliconflow.cn/v1'
siliconflow_auth_token = 'sk-xlnroajavslhhuvfaijqkgqpzzsdqhmmsyzlulvhqhmsrgml'

zhipu_api_key = "ee6c4107dbed41f59843bf796fa1a08f.XidZ1DF5NOr76MzU"
zhipu_api_url = "https://open.bigmodel.cn/api/paas/v4"


# image_generation_url="http://localhost:8000/v1/images/generations"
image_generation_url="https://jimeng.duckcloud.fun/v1/images/generations"
image_api_key = "1dcca7b8288e820e2eb5fe568d1d7d01"

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        return json.load(file)


# config = load_config('config.json')
# api_url = config["api_url"]

# 智谱AI-提交文生视频任务的函数
def submit_video_job(prompt: str, with_audio: bool = True):
    headers = {
        "Authorization": f"Bearer {zhipu_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "cogvideox-flash",
        "quality": "quality",
        "fps": 60,
        "prompt": prompt,
        "with_audio": with_audio
    }
    try:
        response = requests.post(f"{zhipu_api_url}/videos/generations", headers=headers, json=payload, timeout=300)
        if response.status_code != 200:
            logger.error(f"Failed to submit video job. Status code: {response.status_code}, Response: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"Failed to submit video job: {response.text}")

        submit_response = response.json()
        task_id = submit_response.get("id")
        if not task_id:
            raise HTTPException(status_code=500, detail="Failed to get taskId from submit response.")

        logger.info(f"Video generation task submitted successfully. Task ID: {task_id}")
        return task_id

    except Exception as e:
        logger.error(f"An unexpected error occurred while submitting the video job: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# 智谱AI-查询文生视频任务状态的函数
def zp_check_video_status(task_id: str):
    # 正确的请求地址
    status_url = f"https://open.bigmodel.cn/api/paas/v4/async-result/{task_id}"
    headers = {
        "Authorization": f"Bearer {zhipu_api_key}",
        "Content-Type": "application/json",
    }

    start_time = time.time()  # 记录开始时间
    logger.info(f"Checking video status for task ID: {task_id}")

    while True:
        try:
            # 使用 GET 方法，并通过 URL 参数传递 task_id
            response = requests.get(status_url, headers=headers, timeout=300)
            response.raise_for_status()  # 检查请求是否成功
            status_response = response.json()

            task_status = status_response.get("task_status")

            if task_status == "SUCCESS":
                logger.info("Task completed successfully.")
                video_result = status_response.get("video_result", [])
                if video_result:
                    video_url = video_result[0].get("url")
                    cover_image_url = video_result[0].get("cover_image_url")
                    return {"video_url": video_url, "cover_image_url": cover_image_url}
                else:
                    raise HTTPException(status_code=500, detail="Missing video result in SUCCESS response.")

            elif task_status == "PROCESSING":
                elapsed_time = time.time() - start_time  # 计算已处理时间
                logger.info(f"Task is still in progress. Time elapsed: {int(elapsed_time)} seconds.")
                time.sleep(5)  # 等待 5 秒后再次检查

            elif task_status == "FAIL":
                logger.error(f"Task failed. Response: {status_response}")
                raise HTTPException(status_code=500, detail="Task failed during processing.")

            else:
                logger.warning(f"Unexpected status: {task_status}")
                raise HTTPException(status_code=500, detail=f"Unexpected task status: {task_status}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            time.sleep(5)  # 请求失败时也等待 5 秒再重试


def sjld_submit_video_job(api_url, auth_token, model, prompt):
    submit_url = f"{api_url}/video/submit"
    payload = json.dumps({
        "model": model,
        "prompt": prompt
    })
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(submit_url, headers=headers, data=payload)
    return response.json()


# 硅基流动-根据状态获取结果
def gjld_check_video_status(api_url, auth_token, request_id, timeout=200):
    status_url = f"{api_url}/video/status"
    payload = json.dumps({"requestId": request_id})
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    start_time = time.time()
    while True:
        response = requests.post(status_url, headers=headers, data=payload)
        status_response = response.json()
        if status_response.get("status") == "Succeed":
            return status_response
        elif status_response.get("status") == "InProgress":
            if time.time() - start_time > timeout:
                print("Timeout waiting for video status.")
                return None
            time.sleep(5)
        else:
            print("Unexpected status:", status_response.get("status"))
            return None


def generate_timestamp_filenameforaudio(extension='mp3'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename


def save_audio_file(audio_content, output_dir):
    # 生成文件名
    filename = generate_timestamp_filenameforaudio()
    # 组合完整的输出路径
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'wb') as file:
        file.write(audio_content)
    # 返回文件名和输出路径
    return filename, output_path


def upload_cos(region, secret_id, secret_key, bucket, file_name, base_path):
    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key
    )
    client = CosS3Client(config)
    file_path = os.path.join(base_path, file_name)
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=file_path,
        Key=file_name,
        PartSize=10,
        MAXThread=10,
        EnableMD5=False
    )
    if response['ETag']:
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{file_name}"
        return url
    else:
        return None
