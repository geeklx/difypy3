import logging
import os
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from spire.doc import Document, FileFormat
from starlette.responses import JSONResponse

app = FastAPI(title="Markdown to Word Converter")

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarkdownContent(BaseModel):
    content: str


# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
output_dir = os.path.join(current_dir, 'output')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)


@app.post("/office/word/convert")
async def convert_md_to_docx(request: Request):
    logger.info('Received request for /convert')
    content = await request.body()
    if not content:
        logger.error('No content part in the request')
        return JSONResponse(content={"error": "No content part"}, status_code=400)

    content = content.decode('utf-8')
    if content == '':
        logger.error('No content provided')
        return JSONResponse(content={"error": "No content provided"}, status_code=400)

    # 从请求的内容中读取
    mdfile_name = str(int(time.time())) + ".md"
    md_file_path = os.path.join(temp_dir, mdfile_name)
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 创建文档实例
    doc = Document()

    # 从上传的文件加载Markdown内容
    print(md_file_path)
    doc.LoadFromFile(md_file_path, FileFormat.Markdown)

    # 将Markdown文件转换为Word文档并保存
    file_name = str(int(time.time())) + ".docx"
    output_path = os.path.join(output_dir, file_name)
    doc.SaveToFile(output_path, FileFormat.Docx)

    # 释放资源
    doc.Dispose()

    # 清理临时文件
    if os.path.exists(md_file_path):
        os.remove(md_file_path)

    # 返回文件的下载链接
    base_url = str(request.base_url)
    download_url = base_url + 'office/word/download/' + os.path.basename(output_path)
    print(download_url)
    return {"download_url": download_url}


@app.get("/office/word/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(output_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)


def main(arg1: str) -> str:
    import json

    # 解析输入的 JSON 数据
    try:
        data = json.loads(arg1)
    except json.JSONDecodeError:
        return "输入的字符串不是有效的 JSON 格式，请检查输入数据。"

    # 确保解析后的数据包含 'data' 键
    if not isinstance(data, dict) or 'data' not in data:
        return "输入的数据格式不正确，请确保输入是一个包含 'data' 键的 JSON 对象。"

    # 获取 'data' 键对应的数组数据
    image_data = data.get('data', [])

    # 确保 'data' 键的值是一个列表
    if not isinstance(image_data, list):
        return "输入的数据中 'data' 键的值不是一个数组，请确保其值是一个 JSON 数组对象。"

    # 初始化结果字符串
    markdown_result = ""

    # 遍历每条图片数据
    for index, item in enumerate(image_data, start=1):
        # 检查每条数据是否是字典，并且包含 'url' 字段
        if not isinstance(item, dict) or 'url' not in item:
            markdown_result += f"图片第{index}条内容：无法提取 URL（缺少 'url' 字段）\n"
            continue

        # 提取 URL 并生成 Markdown 格式的图片链接
        url = item['url']
        markdown_result += f"![图片{index}]({url})\n"

    # 返回最终的 Markdown 字符串
    return {"result": markdown_result}


def main(arg1: str) -> dict:
    try:
        # 解析外层的 JSON 字符串
        data = json.loads(arg1)

        # 检查 success 字段是否为 True
        if not data.get("success", False):
            return {"error": "操作失败，'success' 字段为 False"}

        # 提取 data 字段中的 video_url
        video_data = data.get("data")
        if not video_data or "video_url" not in video_data:
            return {"error": "JSON 中缺少 'data.video_url' 字段"}

        video_url = video_data["video_url"]

        # 定义文件名（可以根据需要调整）
        filename = "生成视频"

        # 生成 Markdown 格式的 HTML <video> 标签
        markdown_result = f"<video controls><source src='{video_url}' type='video/mp4'>{filename}</video>"

        # 返回结果字典
        return {"result": markdown_result}

    except json.JSONDecodeError:
        return {"error": "无效的 JSON 字符串"}
    except Exception as e:
        return {"error": f"发生未知错误: {str(e)}"}


import json


def main(arg1: str) -> dict:
    try:
        data = json.loads(arg1)
        video_url = data.get("video_url")
        local_url = data.get("local_url")
        markdown_result = f"{video_url}\n<video controls><source src='{video_url}' type='video/mp4'</video>"
        return {"result": markdown_result}
    except json.JSONDecodeError:
        return {"error": "无效的 JSON 字符串"}
    except Exception as e:
        return {"error": f"发生未知错误: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=15015)
