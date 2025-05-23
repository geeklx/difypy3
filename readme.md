



## API 接口详情

### 1. 示例路由

- **Endpoint**: `GET /api/hello`
- **Function**: `say_hello`
- **Description**: 一个简单的示例路由，用于测试服务是否正常运行。
- **Request**: None
- **Response**:
  ```json
  {
    "message": "Hello from APIRouter!"
  }
  ```

### 2. 微软文本转语音 (TTS) - 版本1

- **Endpoint**: `POST /api/edge/tts1`
- **Function**: `generate_tts1`
- **Description**: 使用微软 TTS 服务将文本转换为语音，并返回本地服务器上的音频文件链接。
- **Request Body** (`TTSRequest`):
  ```json
  {
    "model": "tts-1",
    "input": "你好，世界！",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
  }
  ```
- **Response**:
  ```json
  {
    "filename": "<generated_filename>.mp3",
    "output_path": "http://<server_ip>:<port>/static/tts/<generated_filename>.mp3"
  }
  ```

### 3. 微软文本转语音 (TTS) - 上传至腾讯云 COS

- **Endpoint**: `POST /api/edge/tts12`
- **Function**: `generate_tts12`
- **Description**: 使用微软 TTS 服务将文本转换为语音，并将生成的音频文件上传到腾讯云 COS，同时返回 COS链接和本地服务器链接。
- **Request Body** (`TTSRequest`):
  ```json
  {
    "model": "tts-1",
    "input": "你好，腾讯云！",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
  }
  ```
- **Response**:
  ```json
  {
    "audio_url": "https://<tencent_bucket>.cos.<tencent_region>.myqcloud.com/<generated_filename>.mp3",
    "filename": "<generated_filename>.mp3",
    "output_path": "http://<server_ip>:<port>/static/tts/<generated_filename>.mp3",
    "etag": "<cos_etag>"
  }
  ```

### 4. 硅基流动 - 文本转视频

- **Endpoint**: `POST /api/gjld/video`
- **Function**: `sjld_video`
- **Description**: 使用硅基流动 API 根据文本提示生成视频。
- **Request Body** (`VideoSubmission`):
  ```json
  {
    "model": "siliconflow-videomodel-name", 
    "prompt": "一只猫在弹钢琴"
  }
  ```
- **Response**:
  ```json
  {
    "video_url": "<url_to_generated_video>"
  }
  ```

### 5. 硅基流动 - 文本转语音

- **Endpoint**: `POST /api/gjld/audio`
- **Function**: `gjld_audio`
- **Description**: 使用硅基流动 API 将文本转换为语音，并上传到腾讯云 COS。
- **Request Body** (`AudioSubmission`):
  ```json
  {
    "model": "siliconflow-audiomodel-name", 
    "input": "这是硅基流动的声音。",
    "voice": "voice_name" 
  }
  ```
- **Response**:
  ```json
  {
    "filename": "<generated_filename>.mp3",
    "output_path": "https://<tencent_bucket>.cos.<tencent_region>.myqcloud.com/<generated_filename>.mp3"
  }
  ```

### 6. 智谱 AI - 文本转视频

- **Endpoint**: `POST /api/zhipuai/video`
- **Function**: `zpai_video`
- **Description**: 提交一个使用智谱 AI API 的文本转视频生成任务。
- **Request Body** (`VideoRequest`):
  ```json
  {
    "prompt": "日落时分的海滩景色",
    "with_audio": true
  }
  ```
- **Response** (`VideoResponse`): 包含任务 ID、状态和结果视频链接等信息。

### 7. 即梦 - 文本转图像

- **Endpoint**: `POST /api/jimeng/img`
- **Function**: `jm_image`
- **Description**: 使用即梦 API 根据文本提示生成图像。
- **Request Body** (`JMRequest`):
  ```json
  {
    "image_api_key": "<your_jimeng_api_key>",
    "model": "stable-diffusion-xl",
    "prompt": "一个宇航员骑着马在月球上",
    "negativePrompt": "模糊, 低质量",
    "width": 1024,
    "height": 1024,
    "sample_strength": 0.8,
    "image_generation_url": "<jimeng_image_generation_api_endpoint>"
  }
  ```
- **Response**:
  ```json
  {
    "url": "<url_to_generated_image>"
  }
  ```

### 8. 单词比对

- **Endpoint**: `POST /api/dcbd1`
- **Function**: `get_dps123`
- **Description**: 将输入的文本内容发送给 AI 模型进行处理（具体比对逻辑由 `system_prompt` 定义）。
- **Request Body**:
  ```json
  {
    "content": "<text_to_be_processed>"
  }
  ```
- **Response**: AI 模型返回的 JSON 对象。

### 9. ComfyUI BizyAir - 绘画

- **Endpoint**: `POST /api/comfyui_bizyairapi`
- **Function**: `generate_clip_endpoint`
- **Description**: 使用 ComfyUI BizyAir 通过指定工作流文件和参数生成图像。
- **Request**: FormData
  - `prompt` (str): 图像生成提示词。
  - `seed` (int): 随机种子。
  - `idx` (int): 索引。
  - `workflowfile` (UploadFile): ComfyUI 的 JSON 工作流文件。
- **Response**:
  ```json
  {
    "filename": "<generated_filename>.png",
    "output_path": "<url_to_generated_image_on_cos>",
    "etag": "<cos_etag>"
  }
  ```

### 10. Markdown 转 PPT

- **Endpoint**: `POST /api/pptupload`
- **Function**: `upload_markdown`
- **Description**: 上传 Markdown 内容，服务器使用 `marp-cli` 将其转换为 PPTX 文件。
- **Request Body**: Raw Markdown text.
- **Response**: 包含预览链接和下载链接的文本消息。
  ```text
  Markdown 文件已保存
  预览链接: http://<server_ip>:<port>/static/md/<timestamp>.md 
  下载链接: http://<server_ip>:<port>/static/html/<timestamp>.pptx?pptx
  ```

### 11. 网页信息转 Word 文档

- **Endpoint**: `POST /api/generate_doc`
- **Function**: `generate_doc`
- **Description**: 将标题和内容生成为 Word (.docx) 文档。
- **Request Body**:
  ```json
  {
    "title": "文档标题",
    "content": "这是文档的主要内容..."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Document generated successfully",
    "file_path": "http://<server_ip>:<port>/static/html/llm_<timestamp>.docx"
  }
  ```

### 12. Markdown 转思维导图

- **Endpoint**: `POST /api/markdown2map/upload`
- **Function**: `upload_markdown2map`
- **Description**: 上传 Markdown 内容，服务器使用 `markmap-cli` 将其转换为 HTML 思维导图。
- **Request Body**: Raw Markdown text.
- **Response**: 包含预览链接的文本消息或错误信息。
  ```text
  Markdown文件已保存. 点击预览: http://<server_ip>:<port>/static/html/<timestamp>.html
  ```

### 13. 提供 HTML 文件

- **Endpoint**: `POST /api/static/html/{filename}`
- **Function**: `get_html`
- **Description**: 提供指定 HTML 文件的访问路径（主要用于 `markdown2map` 的预览）。
- **Path Parameter**: `filename` (str) - 要访问的 HTML 文件名。
- **Response**: `FileResponse` (HTML 文件内容)。

### 14. 儿童绘本连读（批量处理）

- **Endpoint**: `POST /api/make_ai_txt_picture_audio`
- **Function**: `make_ai_txt_picture_audio`
- **Description**: 批量处理项目，为每个项目生成图像和音频，用于儿童绘本。
- **Request Body**: List of `Item1` objects.
  ```json
  [
    {
      "prompt": "一只可爱的小猫",
      "text_snippet": "这是一只可爱的小猫。"
    },
    {
      "prompt": "一只快乐的小狗",
      "text_snippet": "这是一只快乐的小狗。"
    }
  ]
  ```
- **Response**: List of results, each containing:
  ```json
  {
    "description": "<text_snippet>",
    "image_url": "<url_to_generated_image>",
    "audio_url": "<url_to_generated_audio>"
  }
  ```

### 15. 处理单个绘本项目 (内部调用)

- **Endpoint**: `POST /api/process-data`
- **Function**: `process_data`
- **Description**: (主要由 `/make_ai_txt_picture_audio` 内部调用) 为单个项目生成图像和音频。
- **Request Body** (`Item1`):
  ```json
  {
    "prompt": "一只可爱的小猫",
    "text_snippet": "这是一只可爱的小猫。"
  }
  ```
- **Response**:
  ```json
  {
    "description": "<text_snippet>",
    "image_url": "<url_to_generated_image>",
    "audio_url": "<url_to_generated_audio>"
  }
  ```

### 16. JSON 格式化输出

- **Endpoint**: `POST /api/json1`
- **Function**: `get_json1`
- **Description**: 将输入的 JSON 数据发送给 AI 模型进行处理（具体格式化逻辑由 `system_prompt2` 定义），并返回 JSON 对象。
- **Request Body**: Any valid JSON data.
  ```json
  {
    "key1": "value1",
    "array_key": [1, 2, 3]
  }
  ```
- **Response**: AI 模型返回的 JSON 对象。

### 17. Markdown 转 Word (.docx)

- **Endpoint**: `POST /api/office/word1`
- **Function**: `convert_md_to_docx`
- **Description**: 上传 Markdown 内容，服务器使用 `spire.doc` 库将其转换为 Word 文档。
- **Request Body**: Raw Markdown text.
- **Response**: 包含预览链接的文本消息。
  ```text
  文件已保存. 点击预览: http://<server_ip>:<port>/static/<timestamp>.docx
  ```

### 18. 下载 Word 文件

- **Endpoint**: `GET /api/office/word/download/{filename}`
- **Function**: `download_file`
- **Description**: 下载由 `/office/word1` 生成的 Word 文件。
- **Path Parameter**: `filename` (str) - 要下载的 Word 文件名。
- **Response**: `FileResponse` (Word 文件内容)。

### 19. 即梦 - 文本转视频 (版本1)

- **Endpoint**: `POST /api/jimeng/generate_video`
- **Function**: `generate_video`
- **Description**: 使用即梦 API 根据文本提示生成视频，并上传到腾讯云 COS。需要认证。
- **Authentication**: Requires `Authorization` token via `verify_auth_token`.
- **Request Body** (`VideoRequest2`):
  ```json
  {
    "prompt": "史诗般的太空战斗场面",
    "aspect_ratio": "16:9",
    "fps": 24,
    "duration_ms": 5000
  }
  ```
- **Response**:
  ```json
  {
    "video_url": "<cos_url_to_video>",
    "local_url": "http://<server_ip>:<port>/static/video/<generated_filename>.mp4",
    "task_id": "<jimeng_task_id>",
    "markdown": "<video controls><source src='<cos_url_to_video>' type='video/mp4'>视频预览</video>"
  }
  ```

### 20. BeartAI - 换脸

- **Endpoint**: `POST /api/beartAI/face-swap`
- **Function**: `face_swap`
- **Description**: 使用 BeartAI 服务进行换脸操作。需要认证。
- **Authentication**: Requires `Authorization` token via `verify_auth_token`.
- **Request**: FormData
  - `source_image` (UploadFile): 包含要提取的人脸的源图片。
  - `target_image` (UploadFile): 需要被替换人脸的目标图片。
- **Response**:
  ```json
  {
    "success": true,
    "result_url": "<cos_url_to_swapped_image>",
    "original_url": "http://<server_ip>:<port>/static/img/<generated_filename>.png" 
  }
  ```

### 21. HTML 内容生成与上传

- **Endpoint**: `POST /api/generate-html/`
- **Function**: `generate_html`
- **Description**: 上传 HTML 内容，保存为文件并上传到腾讯云 COS。用于上市公司财报等。需要认证。
- **Authentication**: Requires `Authorization` token via `verify_auth_token`.
- **Request Body** (`HTMLRequest`):
  ```json
  {
    "html_content": "<html><body><h1>Hello World</h1></body></html>",
    "filename": "report.html"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "html_url": "<cos_url_to_html_file>",
    "local_url": "http://<server_ip>:<port>/static/html/<filename>",
    "filename": "<filename>"
  }
  ```

### 22. Gemini - 文本转图像

- **Endpoint**: `POST /api/gemini/generate-image`
- **Function**: `generate_image` (endpoint function)
- **Description**: 使用 Google Gemini API 根据文本提示生成图像，并上传到腾讯云 COS。
- **Request Body** (`GenerateImageRequest`):
  ```json
  {
    "api_key": "<your_gemini_api_key>",
    "model": "gemini-pro-vision", 
    "prompt": "一幅油画风格的日落风景"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": [
      { "type": "text", "content": "<optional_text_response_from_gemini>" },
      { "type": "image", "url": "<cos_url_to_image>", "filename": "<generated_filename>.png" }
    ]
  }
  ```

### 23. Gemini - 图像编辑 (图生图)

- **Endpoint**: `POST /api/gemini/generate-editimage`
- **Function**: `generate_edit_image`
- **Description**: 使用 Google Gemini API 根据文本提示编辑现有图像，并将结果上传到腾讯云 COS。
- **Request Body** (`EditImageRequest`):
  ```json
  {
    "api_key": "<your_gemini_api_key>",
    "model": "gemini-pro-vision", 
    "prompt": "把这只猫变成戴着帽子的猫",
    "image_url": "<url_of_original_image_to_edit>"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": [
      { "type": "text", "content": "<optional_text_response_from_gemini>" },
      { "type": "image", "url": "<cos_url_to_edited_image>", "filename": "<generated_filename>.png" }
    ]
  }
