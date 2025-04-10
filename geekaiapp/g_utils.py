import datetime
import json
import logging
import os
import random
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

import requests
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
from fastapi import HTTPException, Header
from openai import OpenAI
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# config = load_config('config.json')
# api_url = config["api_url"]

# 微软服务
# openai_api_key='zhouhuizhou'
microsoft_api_key = os.getenv('MICROSOFT_API_KEY', 'geekaiapp')
# openai_base_url='https://edgettsapi.duckcloud.fun/v1'
# microsoft_base_url = os.getenv('MICROSOFT_BASE_URL', 'https://edge-tts.g1cloudflare.workers.dev/v1')
microsoft_base_url = os.getenv('MICROSOFT_BASE_URL', 'https://g4.geekaiapp.icu/v1')

# 阿里大模型服务
ai_api_key = os.getenv('ALIYUNCS_API_KEY', 'sk-c59a31cce2c442eaa7fae4790182b5b3')
ai_base_url = os.getenv('ALIYUNCS_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
ai_model = os.getenv('ALIYUNCS_MODEL', 'qwen-max')

# 硅基流动
siliconflow_api_url = os.getenv('SILICONFLOW_API_URL', 'https://api.siliconflow.cn/v1')
siliconflow_auth_token = os.getenv('SILICONFLOW_AUTH_TOEKN', 'sk-xlnroajavslhhuvfaijqkgqpzzsdqhmmsyzlulvhqhmsrgml')
siliconflow_audiomodel = os.getenv('SILICONFLOW_AUDIOMODEL', 'FunAudioLLM/CosyVoice2-0.5B')
siliconflow_voice = os.getenv('SILICONFLOW_VOICE', 'FunAudioLLM/CosyVoice2-0.5B:david')
siliconflow_videomodel = os.getenv('SILICONFLOW_VIDEOMODEL', 'Lightricks/LTX-Video')

# 腾讯oss
tencent_region = os.getenv('TENCENT_REGION', 'ap-nanjing')
tencent_secret_id = os.getenv('TENCENT_SECRET_ID', 'AKID03BB5nRuAD2d0AF7lCPPBl8HCtDNK4d1')
tencent_secret_key = os.getenv('TENCENT_SECRET_KEY', 'EE1by75sSowqZ5NURBrPlutjPt9E9rXD')
tencent_bucket = os.getenv('TENCENT_BUCKET', 'dify-1305874767')

# 智谱AI
zhipu_api_key = os.getenv('ZHIPU_API_KEY', 'ee6c4107dbed41f59843bf796fa1a08f.XidZ1DF5NOr76MzU')
zhipu_api_url = os.getenv('ZHIPU_API_URL', 'https://open.bigmodel.cn/api/paas/v4')

# jimeng
image_generation_url = "http://10.20.0.65:8000/v1/images/generations"
# image_generation_url = os.getenv('IMAGE_GENERATION_URL', 'https://jimeng.duckcloud.fun/v1/images/generations')
image_api_key = os.getenv('IMAGE_API_KEY', '78cd3c79c4a37eb995c26c097a49edb0')
jimeng_cookie = os.getenv('JIMENG_COOKIE',
                          '_tea_utm_cache_513695={%22utm_source%22:%22aigc%22%2C%22utm_medium%22:%22aitools%22%2C%22utm_campaign%22:%22null%22%2C%22utm_content%22:%22hw_jm_aigc%22}; _tea_utm_cache_2018={%22utm_source%22:%22aigc%22%2C%22utm_medium%22:%22aitools%22%2C%22utm_campaign%22:%22null%22%2C%22utm_content%22:%22hw_jm_aigc%22}; fpk1=e25c352638e5c3853f824097b233161e8420bd4fd0cc6196d04de342147d28c86c8f2c791b5b0bd7121f6b813b750f49; n_mh=9W8N-rCI2hHkh4_ypK0jtwSCbLvpXyAXJg5USgpyWj8; store-region=cn-sd; store-region-src=uid; user_spaces_idc={"6978791533491257632":"lf"}; _tea_web_id=7468122294507046438; s_v_web_id=verify_m96qwolo_rNKE9fCE_Ew31_4R0p_APvG_qs7NSnexiubd; passport_csrf_token=43c0f40d17495a6d41aad4f351070357; passport_csrf_token_default=43c0f40d17495a6d41aad4f351070357; sid_guard=78cd3c79c4a37eb995c26c097a49edb0%7C1744010654%7C5184000%7CFri%2C+06-Jun-2025+07%3A24%3A14+GMT; uid_tt=a9c75abaf77a84da67d388dd07379a19; uid_tt_ss=a9c75abaf77a84da67d388dd07379a19; sid_tt=78cd3c79c4a37eb995c26c097a49edb0; sessionid=78cd3c79c4a37eb995c26c097a49edb0; sessionid_ss=78cd3c79c4a37eb995c26c097a49edb0; is_staff_user=false; sid_ucp_v1=1.0.0-KDhhZTRiZDk5MWJjZWY0Y2QyNTJmY2M2NTQyODA1NzcyYmY2M2JmOTQKHQiUpbLthgMQnvvNvwYYn60fIAww_77H3QU4CEAmGgJscSIgNzhjZDNjNzljNGEzN2ViOTk1YzI2YzA5N2E0OWVkYjA; ssid_ucp_v1=1.0.0-KDhhZTRiZDk5MWJjZWY0Y2QyNTJmY2M2NTQyODA1NzcyYmY2M2JmOTQKHQiUpbLthgMQnvvNvwYYn60fIAww_77H3QU4CEAmGgJscSIgNzhjZDNjNzljNGEzN2ViOTk1YzI2YzA5N2E0OWVkYjA; dm_auid=XApD3A/sZyrF4TvjREKyDA==; uifid_temp=88d039951dd94e1f24f0e5162eaa1416b93f52288c2308fe99cb73ebf61507529cb6dacd6831c40ef6b844c6edbf137ac45139bc9850649375e1edd201b6b78ccafe37f6026b25c03c5850211fc55c98; uifid=88d039951dd94e1f24f0e5162eaa1416b93f52288c2308fe99cb73ebf6150752709543fc027b57a3ee8b3f24540c86dfc0f8b636507e41812dce469a5a4524809b0c51c18f6ec4716fc11c994e9639540d1731d5b1d9c56ef05a1f51ffe537af9e768158046fc566f70dda62ab203ce9ee4fde331ac667e0475aca8ec9a03dcd9e38728da5153173c8e0a8444f4b51757a5b8528aef29b80ab708b9b6435f36351d3dfe6d678fea46933dfe98ec9c963; _uetsid=48339540138111f0bb1f8d8eb5af4f7a; _uetvid=580687a0e42f11ef82a2e1047d20e072; odin_tt=cd97196aa9d4f3b97811a3839b109255dab347efb9110de4c0a32dd94947464ee5449c7a2d1fef38eea1e91278e4c36b111f86448ac0c3d6ba015e3154c52e88; ttwid=1|pK3gR8xSUa8okchHBAjXbcO05e7GzLa-4u2iRoCO9q8|1744072190|1c23deac46f008f47ec1007f4f690d934fbfda4f16f7ba4701ac1ec2f62a4f97')
jimeng_sign = os.getenv('JIMENG_SIGN',
                        '_tea_utm_cache_513695={%22utm_source%22:%22aigc%22%2C%22utm_medium%22:%22aitools%22%2C%22utm_campaign%22:%22null%22%2C%22utm_content%22:%22hw_jm_aigc%22}; _tea_utm_cache_2018={%22utm_source%22:%22aigc%22%2C%22utm_medium%22:%22aitools%22%2C%22utm_campaign%22:%22null%22%2C%22utm_content%22:%22hw_jm_aigc%22}; fpk1=e25c352638e5c3853f824097b233161e8420bd4fd0cc6196d04de342147d28c86c8f2c791b5b0bd7121f6b813b750f49; n_mh=9W8N-rCI2hHkh4_ypK0jtwSCbLvpXyAXJg5USgpyWj8; store-region=cn-sd; store-region-src=uid; user_spaces_idc={"6978791533491257632":"lf"}; _tea_web_id=7468122294507046438; s_v_web_id=verify_m96qwolo_rNKE9fCE_Ew31_4R0p_APvG_qs7NSnexiubd; passport_csrf_token=43c0f40d17495a6d41aad4f351070357; passport_csrf_token_default=43c0f40d17495a6d41aad4f351070357; sid_guard=78cd3c79c4a37eb995c26c097a49edb0%7C1744010654%7C5184000%7CFri%2C+06-Jun-2025+07%3A24%3A14+GMT; uid_tt=a9c75abaf77a84da67d388dd07379a19; uid_tt_ss=a9c75abaf77a84da67d388dd07379a19; sid_tt=78cd3c79c4a37eb995c26c097a49edb0; sessionid=78cd3c79c4a37eb995c26c097a49edb0; sessionid_ss=78cd3c79c4a37eb995c26c097a49edb0; is_staff_user=false; sid_ucp_v1=1.0.0-KDhhZTRiZDk5MWJjZWY0Y2QyNTJmY2M2NTQyODA1NzcyYmY2M2JmOTQKHQiUpbLthgMQnvvNvwYYn60fIAww_77H3QU4CEAmGgJscSIgNzhjZDNjNzljNGEzN2ViOTk1YzI2YzA5N2E0OWVkYjA; ssid_ucp_v1=1.0.0-KDhhZTRiZDk5MWJjZWY0Y2QyNTJmY2M2NTQyODA1NzcyYmY2M2JmOTQKHQiUpbLthgMQnvvNvwYYn60fIAww_77H3QU4CEAmGgJscSIgNzhjZDNjNzljNGEzN2ViOTk1YzI2YzA5N2E0OWVkYjA; dm_auid=XApD3A/sZyrF4TvjREKyDA==; uifid_temp=88d039951dd94e1f24f0e5162eaa1416b93f52288c2308fe99cb73ebf61507529cb6dacd6831c40ef6b844c6edbf137ac45139bc9850649375e1edd201b6b78ccafe37f6026b25c03c5850211fc55c98; uifid=88d039951dd94e1f24f0e5162eaa1416b93f52288c2308fe99cb73ebf6150752709543fc027b57a3ee8b3f24540c86dfc0f8b636507e41812dce469a5a4524809b0c51c18f6ec4716fc11c994e9639540d1731d5b1d9c56ef05a1f51ffe537af9e768158046fc566f70dda62ab203ce9ee4fde331ac667e0475aca8ec9a03dcd9e38728da5153173c8e0a8444f4b51757a5b8528aef29b80ab708b9b6435f36351d3dfe6d678fea46933dfe98ec9c963; _uetsid=48339540138111f0bb1f8d8eb5af4f7a; _uetvid=580687a0e42f11ef82a2e1047d20e072; odin_tt=cd97196aa9d4f3b97811a3839b109255dab347efb9110de4c0a32dd94947464ee5449c7a2d1fef38eea1e91278e4c36b111f86448ac0c3d6ba015e3154c52e88; ttwid=1|pK3gR8xSUa8okchHBAjXbcO05e7GzLa-4u2iRoCO9q8|1744072190|1c23deac46f008f47ec1007f4f690d934fbfda4f16f7ba4701ac1ec2f62a4f97')

#
valid_tokens1 = ["sk-geekaiapp", "geekaiapp"]


product_serial = os.getenv('product_serial', '9ec0216f0796254c92dbc2be605a11bb')

# 基础配置
port = int(os.getenv('PORT', '15001'))
ip = os.getenv('IP', 'http://localhost:15001/')
ip_tts = os.getenv('IP_TTS', 'static/tts')
ip_img = os.getenv('IP_IMG', 'static/imgs')
ip_md = os.getenv('IP_MD', 'static/markdown')
ip_html = os.getenv('IP_HTML', 'static/html')
ip_video = os.getenv('IP_VIDEO', 'static/video')
ip_comfyui = os.getenv('IP_COMFYUI', 'static/comfyui')

# current_dir = os.path.dirname(os.path.abspath(__file__))
# static_dir = os.path.join(current_dir, "static")

# if not os.path.exists(SAVE_DIR):
#     os.makedirs(SAVE_DIR)

# 清理临时文件
# if os.path.exists(md_file_path):
#     os.remove(md_file_path)

#
# 设置默认的 MARP_PATH
# os.environ.setdefault("MARP_PATH", "C:/Users/liang/AppData/Roaming/npm/node_modules/@marp-team/marp-cli")
marp_path = os.getenv('MARP_PATH')
# 检查是否获取到了路径
if marp_path:
    print(f"Marp 的路径是: {marp_path}")
else:
    print("未找到 Marp 的路径，请确保环境变量 MARP_PATH 已设置。")

# 基础配置
current_directory = Path.cwd()
# baseurl = current_directory / 'static/'
print("完整路径-current_directory", current_directory)
# path1 = current_directory / ip_tts
# path2 = current_directory / ip_img
# path3 = current_directory / ip_md
# path4 = current_directory / ip_html
# path5 = current_directory / "marp-cli/marp-cli.js"
# print("完整路径-tts:", path1)
# print("完整路径-imgs:", path2)
# print("完整路径-md:", path3)
# print("完整路径-html:", path4)
# print("完整路径-marp-cli:", path5)
# output_path1 = path1
# output_path2 = path2
# marp_path = path5

# 设置工作目录和项目相关的路径
comfyui_endpoit = os.getenv('COMFYUI_ENDPOIT', '127.0.0.1:8188')
WORKING_DIR = current_directory / ip_comfyui
SageMaker_ComfyUI = WORKING_DIR
workflowfile = current_directory / ip_comfyui
COMFYUI_ENDPOINT = comfyui_endpoit

server_address = COMFYUI_ENDPOINT
client_id = str(uuid.uuid4())  # 生成一个唯一的客户端ID

system_prompt = """
你是一位英语教学专家，请根据用户将提供给你的内容，请你分析内容，并提取其中的关键信息，识别出中文对应的英文写错的部分,以 JSON 的形式输出，输出的 JSON 需遵守以下的格式：

示例输入: 
{
    "content": [
        {
            "序号": 1,
            "汉语": "n.哨兵 n./vt.守卫,保卫,看守",
            "英语": "guard"
        },
        {
            "序号": 2,
            "汉语": "vt.保护,护卫 n.安全装置",
            "英语": "safeguard"
        }
    ]
}

JSON 输出示例:
{
  "errors": [
    {
      "序号": <1>,
      "汉语": <n.保证(书),保修单 vt.保证,提供(产品)保修单>,
      "错误英语": <gooe>,
      "正确英语": <gruarantee>
    }
  ]
}
"""

system_prompt2 = """
你是一位代码编程专家，请根据用户将提供给你的内容，请你分析内容，提取其中的关键信息，以 JSON 的形式输出，输出的 JSON 需遵守以下的格式：

示例输入:
{
    "content": [
        {
            "序号": 1,
            "汉语": "n.哨兵 n./vt.守卫,保卫,看守",
            "英语": "guard"
        },
        {
            "序号": 2,
            "汉语": "vt.保护,护卫 n.安全装置",
            "英语": "safeguard"
        }
    ]
}

JSON 输出示例:
{
"name": <候选人姓名>,
"email": <候选人邮箱地址>,
"code": <候选人分数（1-100）>,
"txt": <[候选人资格和适合程度的简要概述]\n[提供 2-3 句话的总体建议，例如优先考虑哪些候选人进行面试或对候选人库的任何一般性观察]>
}
"""


def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        return json.load(file)


# 智谱AI-提交文生视频任务的函数
def zpai_video_job(prompt: str, with_audio: bool = True):
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
def zpai_check_video_status(task_id: str):
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


# 硅基流动文生音
def gjld_submit_video_job(api_url, auth_token, model, prompt):
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


# 随机给名字
def generate_timestamp_filenameforaudio(extension='mp3'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename


# 保存文件
def save_audio_file(audio_content, output_dir):
    # 生成文件名
    filename = generate_timestamp_filenameforaudio()
    # 组合完整的输出路径
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'wb') as file:
        file.write(audio_content)
    # 返回文件名和输出路径
    return filename, output_path


# 上传腾讯oss
def upload_cos(env, region, secret_id, secret_key, bucket, file_name, base_path):
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


# 定义一个函数来显示GIF图片
def show_gif(fname):
    import base64
    from IPython import display
    with open(fname, 'rb') as fd:
        b64 = base64.b64encode(fd.read()).decode('ascii')
    return display.HTML(f'<img src="data:image/gif;base64,{b64}" />')


# 定义一个函数向服务器队列发送提示信息
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())


# 定义一个函数来获取图片
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()


# 定义一个函数来获取历史记录
def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())


# 定义一个函数来获取图片，这涉及到监听WebSocket消息
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    logger.info(f"Prompt ID: {prompt_id}")
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    logger.info("Execution completed")
                    break  # 执行完成
        else:
            continue  # 预览为二进制数据

    history = get_history(prompt_id)[prompt_id]
    logger.info(f"History: {history}")
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        # 图片分支
        if 'images' in node_output:
            images_output = []
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
            output_images[node_id] = images_output
        # 视频分支
        if 'videos' in node_output:
            videos_output = []
            for video in node_output['videos']:
                video_data = get_image(video['filename'], video['subfolder'], video['type'])
                videos_output.append(video_data)
            output_images[node_id] = videos_output

    logger.info("Images retrieved successfully")
    return output_images


# 解析工作流并获取图片
def parse_worflow(ws, prompt, seed, workflowfile):
    logger.info(f"Workflow file: {workflowfile}")
    # with open(workflowfile, 'r', encoding="utf-8") as workflow_api_txt2gif_file:
    #     prompt_data = json.load(workflow_api_txt2gif_file)
    # 设置文本提示
    workflowfile["80"]["inputs"]["text"] = prompt
    return get_images(ws, workflowfile)


# 生成图像并显示
def generate_clip(prompt, seed, workflowfile, idx):
    logger.info(f"Seed: {seed}")
    ws = websocket.WebSocket()
    try:
        ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
        logger.info("WebSocket connected successfully")
    except Exception as e:
        logger.error(f"WebSocket connection failed: {e}")
        raise

    images = parse_worflow(ws, prompt, seed, workflowfile)

    for node_id in images:
        for image_data in images[node_id]:
            # 获取当前时间，并格式化为 YYYYMMDDHHMMSS 的格式
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{idx}_{seed}_{timestamp}.png"
            # 使用格式化的时间戳在文件名中
            GIF_LOCATION = os.path.join(current_directory / ip_img, filename)
            img_url = f"{ip}{ip_img}/{filename}"
            logger.info(f"Saving image to: {GIF_LOCATION}")
            with open(GIF_LOCATION, "wb") as binary_file:
                # 写入二进制文件
                binary_file.write(image_data)

            show_gif(GIF_LOCATION)
            # 上传腾讯oss存储
            etag = upload_cos('test', tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket, filename,
                              current_directory / ip_img)
            logger.info(f"{GIF_LOCATION} DONE!!!")
            logger.info(f"{etag} DONE!!!")
    return filename, img_url, etag


# 绘本故事图片
async def generate_image(prompt: str):
    headers = {
        "Authorization": f"Bearer {image_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jimeng-2.1",
        "prompt": prompt,
        "negativePrompt": "",
        "width": 1024,
        "height": 1024,
        "sample_strength": 0.5,
    }
    try:
        response = requests.post(image_generation_url, headers=headers, json=data)
        response.raise_for_status()  # 检查 HTTP 状态码
        result = response.json()
        return result["data"][0]["url"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"图像生成 API 请求失败: {e}")
    except (KeyError, IndexError) as e:
        raise Exception(f"图像生成 API 响应解析失败: {e}")


# 绘本故事音频
async def generate_tts(text_snippet: str, client: OpenAI):
    """
    Generates text-to-speech audio using the edge tts API and uploads it to Tencent Cloud COS.
    """
    try:
        data = {
            'model': 'tts-1',
            'input': text_snippet,
            'voice': 'zh-CN-XiaoxiaoNeural',
            'response_format': 'mp3',
            'speed': '1.0',
        }
        response = client.audio.speech.create(
            **data
        )
        # Save the audio file
        filename, output_path2 = save_audio_file(response.content, current_directory / ip_tts)
        audio_url = f"{ip}{ip_tts}/{filename}"
        return audio_url
        # Upload to COS
        # etag = upload_cos(region, secret_id, secret_key, bucket, filename, output_path)
        # if etag:
        #     audio_url = f"https://{bucket}.cos.{region}.myqcloud.com/{filename}"
        #     return audio_url
        # else:
        #     raise HTTPException(status_code=500, detail="Failed to upload audio to COS")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def verify_auth_token(authorization: str = Header(None)):
    """验证 Authorization Header 中的 Bearer Token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization Scheme")

    # 从配置文件读取有效token列表
    # valid_tokens = json.loads(valid_tokens1)
    if token not in valid_tokens1:
        raise HTTPException(status_code=403, detail="Invalid or Expired Token")

    return token


# 修改视频生成接口，添加鉴权依赖
# 添加新的辅助函数
def generate_timestamp_filename_for_video(extension='mp4'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"video_{timestamp}_{random_number}.{extension}"
    return filename


def download_video(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filename = generate_timestamp_filename_for_video()
    file_path = os.path.join(output_path, filename)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    return filename, file_path

def download_image(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filename = generate_timestamp_filename_for_image()
    file_path = os.path.join(output_path, filename)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    return filename, file_path


def generate_timestamp_filename_for_image(extension='jpg'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"faceswap_{timestamp}_{random_number}.{extension}"
    return filename
