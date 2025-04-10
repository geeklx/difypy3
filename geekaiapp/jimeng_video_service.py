import logging

from fastapi import FastAPI, Header
from fastapi_mcp import add_mcp_server

from geekaiapp.g_jiekou import generate_video
from geekaiapp.g_model import VideoRequest2
from geekaiapp.g_utils import verify_auth_token

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Jimeng Video Service API",
    description="一个用于生成AI视频的服务 API",
    version="1.0.0",
)

# 修改 MCP 服务器配置
mcp_server = add_mcp_server(
    app,
    mount_path="/mcp",
    name="Jimeng Video MCP",
    description="集成了智能视频生成功能的 MCP 服务",
    base_url="http://localhost:15123"
)


# 添加自定义 MCP 工具
@mcp_server.tool()
async def generate_video_mcp(
        prompt: str,
        aspect_ratio: str = "16:9",
        duration_ms: int = 5000,
        fps: int = 24,
        authorization: str = Header(...)
) -> dict:
    """
    生成一个基于文本提示的 AI 视频。

    Args:
        prompt: 用于生成视频的文本提示词
        aspect_ratio: 视频宽高比，默认为 "16:9"
        duration_ms: 视频时长（毫秒），默认为 5000
        fps: 视频帧率，默认为 24
        authorization: Bearer token 用于认证（必填）

    Returns:
        dict: 包含以下字段的字典：
            - video_url: 生成视频的 URL
            - task_id: 任务 ID
            - markdown: 视频预览的 markdown 代码
    """
    request = VideoRequest2(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        duration_ms=duration_ms,
        fps=fps
    )
    return await generate_video(request, auth_token=verify_auth_token(authorization))


if __name__ == "__main__":
    import uvicorn

    # 修改启动配置
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=15123,
        log_level="info",
        reload=False  # 禁用热重载以避免初始化问题
    )
