import uvicorn
from fastapi import FastAPI

from model_jk import router as router_edgetts

app = FastAPI()

app.include_router(router_edgetts)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5037)
