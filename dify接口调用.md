# 1 工作流调用

  我们可以使用curl  命令实现工作流的调用

```shell
curl --location --request POST 'http://14.103.204.132/v1/workflows/run' \
--header 'Authorization: Bearer app-YwwJyPLw77fTIZaAag5cjLY5' \
--header 'Content-Type: text/plain' \
--data-raw '{
     "inputs": {
         "prompt": "小马过河"
     },
     "response_mode": "streaming",
     "user": "abc-123"
 }'
```

 

# 2  chatflow调用

  我们可以使用curl  命令实现工作流的调用,其中输入参数是一个下拉选项，我这里定义一个参数名称叫做type

  ![image-20250610112338909](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250610112338909.png)

curl  命令

```shell
curl --location --request POST 'http://14.103.204.132/v1/chat-messages' \
--header 'Authorization: Bearer app-PDVTo4hKjTuTt2EPunwxPHo4' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {
        "type": "36kr"
    },
    "query": "测试内容",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123"
}'
```

解释一下 inputs  里面需要有个type 和上面工作流配置type 对应， 外面的query 是对话用到的 请求参数需要有这个参数。

参考接口文档

![image-20250610112712700](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250610112712700.png)

​        使用postman测试

   ![image-20250610112741296](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250610112741296.png)



 如果需要返回详细信息，需要response_mode=blocking

 修改命令如下

```shell
curl --location --request POST 'http://14.103.204.132/v1/chat-messages' \
--header 'Authorization: Bearer app-PDVTo4hKjTuTt2EPunwxPHo4' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {
        "type": "36kr"
    },
    "query": "测试内容",
    "response_mode": "blocking",
    "conversation_id": "",
    "user": "abc-123"
}'
```

![image-20250610113625198](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250610113625198.png)

## 2.1 获取会话历史消息

 如果我们需要获取历史会话消息

```shell
curl -X GET 'http://14.103.204.132/v1/messages?user=abc-123&conversation_id=d368493a-4544-4aff-8651-f23b602c2d58' \
--header 'Authorization: Bearer app-PDVTo4hKjTuTt2EPunwxPHo4'
```

![image-20250610113926641](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250610113926641.png)