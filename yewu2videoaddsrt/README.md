
# 一键创建解说短视频/视频总结

利用 GeminiAI 大模型，一键为长视频创建解说短视频或视频总结。同时可支持使用三步反思法翻译字幕 & 音视频转录字幕


## 功能特性

- 一键为长视频创建解说短视频。
- 制作视频总结
- 支持三步反思法翻译SRT字幕
- 支持音视频转录为SRT字幕
 
## 界面

![image](https://github.com/user-attachments/assets/aeb39f4f-9eb0-4c5d-b776-386a67b99a22)


启动将在web浏览器打开一个单页 `http://127.0.0.1:5030`. 可执行解说视频创建、字幕翻译或音视频转录操作

## 注意事项

1. 必须要有牢靠的梯子，尤其视频解说，如果梯子不稳，难以成功
2. 核心是提示词，可自行修改提示词实现更好效果
3. 依赖GeminiAI，可去申请免费Key，建议使用 gemini-1.5-flash模型，免费额度高
4. 可能遇到的问题大部分原因都是梯子不稳导致


## 部署

**Windows**




**Linux和Mac**


```


cd ai2srt

python3 -m venv venv 


source ./venv/bin/activate

pip3 install -r requirements.txt


python3 app.py


```



