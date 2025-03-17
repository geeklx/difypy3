# 使用官方 Python 3.13 镜像
#FROM python:3.13-slim
#FROM mirrors.cloud.tencent.com/python/python:3.13-slim
#FROM registry.cn-hangzhou.aliyuncs.com/luyuehm/python:3.13-slim
FROM crpi-oz87fnf8zm051s5l.cn-hangzhou.personal.cr.aliyuncs.com/geekaiapp/python:3.13-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到 container 中
COPY requirements.txt /app
COPY readme.txt /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 运行应用程序
CMD ["python", "geekaiapp/model_jk.py"]


#docker-compose up --build