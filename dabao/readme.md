以下是基于提供的代码内容编写的符合 `curl` 格式的文档，并支持在 Postman 中直接使用。每个 API 端点都包含了请求方法、URL、请求头、请求体等信息。

### 1. 微软的文生音，并上传到腾讯云 COS
**Endpoint:** `/edge/tts12/`

**Method:** `POST`

**URL:** `http://<your-server-ip>:<port>/edge/tts12/`

**Headers:**
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "model": "tts-1",
    "input": "Hello, this is a test.",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
}
```

**Curl Command:**
```bash
curl -X POST "http://<your-server-ip>:<port>/edge/tts12/" \
-H "Content-Type: application/json" \
-d '{
    "model": "tts-1",
    "input": "Hello, this is a test.",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
}'
```

### 2. 微软的文生音
**Endpoint:** `/edge/tts1/`

**Method:** `POST`

**URL:** `http://<your-server-ip>:<port>/edge/tts1/`

**Headers:**
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "model": "tts-1",
    "input": "Hello, this is a test.",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
}
```

**Curl Command:**
```bash
curl -X POST "http://<your-server-ip>:<port>/edge/tts1/" \
-H "Content-Type: application/json" \
-d '{
    "model": "tts-1",
    "input": "Hello, this is a test.",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
}'
```

### 3. 硅基流动-文生视频
**Endpoint:** `/gjld/video/`

**Method:** `POST`

**URL:** `http://<your-server-ip>:<port>/gjld/video/`

**Headers:**
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "model": "video-model",
    "prompt": "A beautiful sunset over the mountains."
}
```

**Curl Command:**
```bash
curl -X POST "http://<your-server-ip>:<port>/gjld/video/" \
-H "Content-Type: application/json" \
-d '{
    "model": "video-model",
    "prompt": "A beautiful sunset over the mountains."
}'
```

### 4. 硅基流动-文生音
**Endpoint:** `/gjld/audio/`

**Method:** `POST`

**URL:** `http://<your-server-ip>:<port>/gjld/audio/`

**Headers:**
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "model": "audio-model",
    "input": "Hello, this is a test.",
    "voice": "alloy",
    "response_format": "mp3",
    "sample_rate": 32000,
    "stream": true,
    "speed": 1,
    "gain": 0
}
```

**Curl Command:**
```bash
curl -X POST "http://<your-server-ip>:<port>/gjld/audio/" \
-H "Content-Type: application/json" \
-d '{
    "model": "audio-model",
    "input": "Hello, this is a test.",
    "voice": "alloy",
    "response_format": "mp3",
    "sample_rate": 32000,
    "stream": true,
    "speed": 1,
    "gain": 0
}'
```

### 5. 智谱AI-提交文生视频任务
**Endpoint:** `/zhipuai/video/`

**Method:** `POST`

**URL:** `http://<your-server-ip>:<port>/zhipuai/video/`

**Headers:**
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "prompt": "A beautiful sunset over the mountains.",
    "with_audio": true
}
```

**Curl Command:**
```bash
curl -X POST "http://<your-server-ip>:<port>/zhipuai/video/" \
-H "Content-Type: application/json" \
-d '{
    "prompt": "A beautiful sunset over the mountains.",
    "with_audio": true
}'
```

### 6. 即梦-文生图
**Endpoint:** `/jimeng/img/`

**Method:** `POST`

**URL:** `http://<your-server-ip>:<port>/jimeng/img/`

**Headers:**
- `Content-Type: application/json`
- `Authorization: Bearer <your-api-key>`

**Body (JSON):**
```json
{
    "model": "image-model",
    "prompt": "A beautiful sunset over the mountains.",
    "negativePrompt": "dark, gloomy",
    "width": 1024,
    "height": 768,
    "sample_strength": 0.75
}
```

**Curl Command:**
```bash
curl -X POST "http://<your-server-ip>:<port>/jimeng/img/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your-api-key>" \
-d '{
    "model": "image-model",
    "prompt": "A beautiful sunset over the mountains.",
    "negativePrompt": "dark, gloomy",
    "width": 1024,
    "height": 768,
    "sample_strength": 0.75
}'
```

### 7. 单词比对
**Endpoint:** `/dcbd1/`

**Method:** `POST`

**URL:** `http://<your-server-ip>:<port>/dcbd1/`

**Headers:**
- `Content-Type: application/json`

**Body (JSON):**
```json
{
    "content": "Compare these words."
}
```

**Curl Command:**
```bash
curl -X POST "http://<your-server-ip>:<port>/dcbd1/" \
-H "Content-Type: application/json" \
-d '{
    "content": "Compare these words."
}'
```

### 注意事项：
- 替换 `<your-server-ip>` 和 `<port>` 为实际的服务器 IP 地址和端口号。
- 替换 `<your-api-key>` 为实际的 API 密钥。
- 确保服务器已启动并监听指定的端口。

这些 `curl` 命令可以直接在终端中运行，也可以在 Postman 中导入为请求集合。