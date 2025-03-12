import requests
from fastapi import FastAPI, HTTPException, APIRouter
from openai import OpenAI

from dabao.cos_model import TTSRequest, VideoSubmission, AudioSubmission, VideoRequest, VideoResponse, JMRequest
# sys.path.append('path/to/dabao')  # 添加模块路径到搜索路径
from dabao.cos_utils import openai_api_key1, openai_base_url1, port1, ip1, region1, secret_id1, secret_key1, bucket1, \
    save_audio_file, upload_cos, videomodel, submit_video_job, siliconflow_api_url, siliconflow_auth_token, \
    audiomodel, voice, logger, output_path1, sjld_submit_video_job, gjld_check_video_status, zp_check_video_status

app = FastAPI()

router = APIRouter()

# 基础配置
api_key = openai_api_key1
base_url = openai_base_url1
output_path = output_path1
port = port1
ip = ip1

# Tencent Cloud COS configuration
region = region1
secret_id = secret_id1
secret_key = secret_key1
bucket = bucket1

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


# 微软的文生音，并上传到腾讯oss
@router.post("/edgetts12/")
async def generate_tts(request_body: TTSRequest):
    """
    Generates text-to-speech audio using the edge tts API and uploads it to Tencent Cloud COS.
    """
    try:
        data = {
            'model': request_body.model,
            'input': request_body.input,
            'voice': request_body.voice,
            'response_format': request_body.response_format,
            'speed': request_body.speed,
        }
        response = client.audio.speech.create(
            **data
        )
        # Save the audio file
        filename, output_path2 = save_audio_file(response.content, output_path)
        ip = 'http://192.168.2.2:5031/dabaotmp1'
        audio_url2 = f"{ip}/{filename}"
        # Upload to COS
        etag = upload_cos(region, secret_id, secret_key, bucket, filename, output_path)
        if etag:
            audio_url = f"https://{bucket}.cos.{region}.myqcloud.com/{filename}"
            return {
                "audio_url": audio_url,
                "filename": filename,
                "output_path": audio_url2,
                "etag": etag
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to upload audio to COS")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 微软的文生音1
@router.post('/edgetts1/')
async def generate_tts(request_body: TTSRequest):
    try:
        data = {
            'model': request_body.model,
            'input': request_body.input,
            'voice': request_body.voice,
            'response_format': request_body.response_format,
            'speed': request_body.speed,
        }
        response = client.audio.speech.create(
            **data
        )
        filename, output_path2 = save_audio_file(response.content, output_path)
        ip = 'http://192.168.31.116:5052/tts1'
        audio_url2 = f"{ip}/{filename}"
        return {
            "filename": filename,
            "output_path": audio_url2
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# 硅基流动-文生视频
@router.post("/submit-video/")
async def sjld_submit_video(video_submission: VideoSubmission):
    # Use the model from the user input if provided, otherwise use the default from config
    model = video_submission.model if video_submission.model else videomodel

    submit_response = sjld_submit_video_job(siliconflow_api_url, siliconflow_auth_token, model, video_submission.prompt)
    if "error" in submit_response:
        raise HTTPException(status_code=500, detail=submit_response["error"])

    request_id = submit_response.get("requestId")
    if not request_id:
        raise HTTPException(status_code=500, detail="Failed to get requestId from submit response.")

    status_response = gjld_check_video_status(siliconflow_api_url, siliconflow_auth_token, request_id)
    if status_response and status_response.get("status") == "Succeed" and status_response.get("results") and \
            status_response["results"].get("videos") and len(status_response["results"]["videos"]) > 0:
        video_url = status_response['results']['videos'][0]['url']
        return {"video_url": video_url}
    else:
        raise HTTPException(status_code=500, detail="Invalid status response or missing video URL.")


# 硅基流动-文生音
@router.post("/generate-audio/")
async def generate_audio(audio_Submission: AudioSubmission):
    audiourl = siliconflow_api_url + "/audio/speech"
    audiomodel2 = audio_Submission.model if audio_Submission.model else audiomodel
    voice2 = audio_Submission.voice if audio_Submission.voice else voice
    headers = {
        "Authorization": f"Bearer {siliconflow_auth_token}",
        "Content-Type": "application/json"
    }
    data = {
        "model": audiomodel2,
        "input": audio_Submission.input,
        "voice": voice2,
        "response_format": "mp3",
        "sample_rate": 32000,
        "stream": True,
        "speed": 1,
        "gain": 0
    }
    response = requests.post(audiourl, headers=headers, json=data)

    if response.status_code == 200:
        filename, output_path2 = save_audio_file(response.content, output_path)
        ip = 'http://10.20.0.65:5055/g2'
        audio_url2 = f"{ip}/{filename}"
        return {
            "filename": filename,
            "output_path": audio_url2
        }
        # env = 'test'
        # etag = upload_cos(env, filename, output_path)
        # return {
        #     "filename": filename,
        #     "output_path": output_path2,
        #     "etag": etag
        # }
    else:
        raise HTTPException(status_code=response.status_code, detail="请求失败")


# 智谱AI-提交文生视频任务的接口
@router.post("/zhipuai/video/")
async def submit_video(video_request: VideoRequest):
    """Submits a text-to-video generation job using the ZhipuAI API."""
    try:
        task_id = submit_video_job(video_request.prompt, video_request.with_audio)
        logger.info(f"Video generation task submitted successfully. Task ID: {task_id}")

        # 检查任务状态并返回结果
        status_response = zp_check_video_status(task_id)
        return VideoResponse(**status_response)

    except HTTPException as err:
        raise err
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# 即梦-文生图的接口
@router.post("/jimeng/img/")
async def generate_image(request1: JMRequest):
    headers = {
        "Authorization": f"Bearer {request1.image_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": request1.model,
        "prompt": request1.prompt,
        "negativePrompt": request1.negativePrompt,
        "width": request1.width,
        "height": request1.height,
        "sample_strength": request1.sample_strength,
    }
    try:
        response = requests.post(request1.image_generation_url, headers=headers, json=data)
        response.raise_for_status()  # 检查 HTTP 状态码
        result = response.json()
        return result["data"][0]["url"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"图像生成 API 请求失败: {e}")
    except (KeyError, IndexError) as e:
        raise Exception(f"图像生成 API 响应解析失败: {e}")

# import uvicorn
#
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=5036)
