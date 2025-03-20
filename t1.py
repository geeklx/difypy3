import re
import time

import requests


def main(json_html: str, apikey: str, apiurl: str, strtype: str) -> dict:
    try:
        # 去除输入字符串中的 ```html 和 ``` 标记
        html_content = re.sub(r'^```html\s*|\s*```$', '', json_html, flags=re.DOTALL).strip()

        # 生成时间戳，确保文件名唯一
        timestamp = int(time.time())
        filename = f"{strtype}_{timestamp}.html"

        # API端点（假设本地运行）
        url = f"{apiurl}"

        # 请求数据
        payload = {
            "html_content": html_content,
            "filename": filename  # 使用传入的文件名
        }

        # 设置请求头（包含认证token）
        headers = {
            "Authorization": f"Bearer {apikey}",  # 替换为实际的认证token
            "Content-Type": "application/json"
        }

        try:
            # 发送POST请求
            response = requests.post(url, json=payload, headers=headers)

            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                html_url = result.get("html_url", "")
                local_url = result.get("local_url", "")
                generated_filename = result.get("filename", "")

                # 返回结果
                return {
                    "html_url": html_url,
                    "local_url": local_url,
                    "filename": generated_filename,
                    "markdown_result": f"[点击查看oss]({html_url}\n[点击查看本地]({local_url})"
                }
            else:
                raise Exception(f"HTTP Error: {response.status_code}, Message: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    except Exception as e:
        return {
            "error": f"Error: {str(e)}"
        }
