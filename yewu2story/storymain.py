from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api.video import router as video_router

app = FastAPI()
# 先挂载静态文件
app.mount("/tasks", StaticFiles(directory="tasks"), name="tasks")

# Include the video router
app.include_router(video_router, prefix="")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=15003)