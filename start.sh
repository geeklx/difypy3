#!/bin/bash
python geekaiapp/g_jiekou.py &
python geekaiapp/jimeng_video_service.py &
python yewu2edgetts/app.py &
python yewu2googleimgtxt/image-generation-server.py &
python yewu2story/videostart.py &
python yewu2videoaddsrt/app.py &
wait  # 等待所有后台进程完成