# 使用说明文档

## 概述

本文档提供了基于 FastAPI 构建的 API 服务的使用说明。该服务集成了多种功能，包括文本转语音、文本转视频、图像生成、Markdown 转 PPT、网页信息生成 Word 文档等。以下将详细介绍每个接口的使用方法。

## 安装与运行

### 依赖安装

在运行项目之前，请确保已安装所需的 Python 依赖包。可以通过以下命令安装：

```bash
pip install -r requirements.txt
```

### 运行服务

在项目根目录下运行以下命令启动服务：

```bash
python main.py
```

服务启动后，默认监听 `0.0.0.0` 的 `port` 端口（具体端口号请查看配置文件）。

## API 接口说明

### 1. 微软文本转语音 (TTS)

#### 1.1 生成语音并保存到本地

- **接口路径**: `/edge/tts1/`
- **请求方法**: `POST`
- **请求体**:

```json
{
  "model": "模型名称",
  "input": "输入文本",
  "voice": "语音类型",
  "response_format": "音频格式",
  "speed": "语速"
}
```

- **响应**:

```json
{
  "filename": "文件名",
  "output_path": "音频文件URL"
}
```

#### 1.2 生成语音并上传到腾讯云 COS

- **接口路径**: `/edge/tts12/`
- **请求方法**: `POST`
- **请求体**: 同上
- **响应**:

```json
{
  "audio_url": "COS音频文件URL",
  "filename": "文件名",
  "output_path": "本地音频文件URL",
  "etag": "COS返回的ETag"
}
```

### 2. 硅基流动文本转视频

- **接口路径**: `/gjld/video/`
- **请求方法**: `POST`
- **请求体**:

```json
{
  "model": "模型名称",
  "prompt": "生成视频的文本提示"
}
```

- **响应**:

```json
{
  "video_url": "生成的视频URL"
}
```

### 3. 硅基流动文本转语音

- **接口路径**: `/gjld/audio/`
- **请求方法**: `POST`
- **请求体**:

```json
{
  "model": "模型名称",
  "input": "输入文本",
  "voice": "语音类型"
}
```

- **响应**:

```json
{
  "filename": "文件名",
  "output_path": "音频文件URL"
}
```

### 4. 智谱AI文本转视频

- **接口路径**: `/zhipuai/video/`
- **请求方法**: `POST`
- **请求体**:

```json
{
  "prompt": "生成视频的文本提示",
  "with_audio": "是否包含音频"
}
```

- **响应**:

```json
{
  "task_id": "任务ID",
  "status": "任务状态",
  "video_url": "生成的视频URL"
}
```

### 5. 即梦文生图

- **接口路径**: `/api/jimeng/img/`
- **请求方法**: `POST`
- **请求体**:

```json
{
  "image_api_key": "API密钥",
  "model": "模型名称",
  "prompt": "生成图像的文本提示",
  "negativePrompt": "负面提示",
  "width": "图像宽度",
  "height": "图像高度",
  "sample_strength": "采样强度"
}
```

- **响应**:

```json
{
  "url": "生成的图像URL"
}
```

### 6. 单词比对

- **接口路径**: `/dcbd1/`
- **请求方法**: `POST`
- **请求体**:

```json
{
  "content": [
    {
      "序号": 1,
      "汉语": "中文解释",
      "英语": "英文单词"
    }
  ]
}
```

- **响应**:

```json
{
  "errors": [
    {
      "序号": 1,
      "汉语": "中文解释",
      "错误英语": "错误的英文单词",
      "正确英语": "正确的英文单词"
    }
  ]
}
```

### 7. BizyAI 绘画 (ComfyUI)

- **接口路径**: `/comfyui_bizyairapi/`
- **请求方法**: `POST`
- **请求体**:

```form-data
prompt: 生成图像的提示
seed: 随机种子
idx: 索引
workflowfile: 工作流文件 (JSON)
```

- **响应**:

```json
{
  "filename": "文件名",
  "output_path": "生成的图像URL",
  "etag": "COS返回的ETag"
}
```

### 8. Markdown 转 PPT

- **接口路径**: `/pptupload/`
- **请求方法**: `POST`
- **请求体**: Markdown 文件内容
- **响应**:

```text
Markdown 文件已保存
预览链接: <Markdown文件URL>
下载链接: <PPT文件URL>
```

### 9. 网页信息生成 Word 文档

- **接口路径**: `/generate_doc/`
- **请求方法**: `POST`
- **请求体**:

```json
{
  "title": "文档标题",
  "content": "文档内容"
}
```

- **响应**:

```json
{
  "message": "Document generated successfully",
  "file_path": "生成的Word文档URL"
}
```

### 10. Markdown 转 HTML 思维导图

- **接口路径**: `/markdown2map/upload/`
- **请求方法**: `POST`
- **请求体**: Markdown 文件内容
- **响应**:

```text
Markdown文件已保存. 点击预览: <HTML文件URL>
```

### 11. 获取 HTML 文件

- **接口路径**: `/static/html/{filename}`
- **请求方法**: `GET`
- **响应**: 返回指定的 HTML 文件内容

## 错误处理

所有接口在发生错误时都会返回 HTTP 500 状态码，并在响应体中包含错误信息。例如：

```json
{
  "detail": "错误信息"
}
```

## 日志

服务运行时会记录日志，日志级别为 `INFO`，日志信息会输出到控制台。

## 结语

以上是 API 服务的详细使用说明。如有任何问题，请联系开发者。