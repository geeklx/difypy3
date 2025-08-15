def main(arg1: str) -> dict:
    # arg1 = "```json\n{\n  \"始发站\": \"南京南\",\n  \"终点站\": \"北京南\",\n  \"车次\": \"G124\",\n  \"出发时间\": \"2015年07月10日 10:21\",\n  \"票价\": \"¥435.5\",\n  \"身份证号\": \"3412261995********\",\n  \"姓名\": \"曹云\"\n}\n```"
    table = [[arg1]]
    result_str = str(table).replace("'", '"')
    result_str = result_str.replace("\\n", "\n")
    result_str = result_str.replace('\"```json', '"```json')
    result_str = result_str.replace('```\"', '```"')
    return {
        "result": result_str,
    }


def main22(arg1: str) -> dict:
    import json
    data = json.loads(arg1)
    str1 = data['text']
    table = [[str1]]
    result_str = str(table).replace("'", "\"")
    # 返回结果
    return {
        "result": result_str,
    }


def main(arg1: str) -> dict:
    str1 = arg1
    table = [[str1]]
    # 将表格转换为字符串形式的嵌套列表，并添加转义字符
    result_str = str(table).replace("'", '"')
    result_str = result_str.replace('\"```json', '"```json')
    # 返回结果
    return {
        "result": result_str,
    }


def main1(arg1: str) -> dict:
    arg1 = "[[\"{  \"始发站\": \"南京南\",  \"终点站\": \"北京南\",  \"车次\": \"G124\",  \"出发时间\": \"2015年07月10日 10:21\",  \"票价\": \"¥435.5\",  \"身份证号\": \"3412261995********\",  \"姓名\": \"曹云\"}\"]]"
    result_str = arg1.replace("'", "\"")
    return {
        "result": result_str,
    }


def main111(base_url: str = 'http://127.0.0.1:9090') -> dict:
    """
    测试获取班级平均分接口。

    :param base_url: API基础URL，默认为'http://127.0.0.1:9090'
    :return: 包含班级平均分数据或错误信息的字典
    """
    # 设置请求的URL
    url = f'{base_url}/db/class/average-scores'

    try:
        # 发送GET请求
        response = requests.get(url)

        # 检查响应状态码
        if response.status_code == 200:
            averages = response.json()

            # 如果数据为空，返回无数据提示
            if not averages:
                markdown_result = "无数据可显示。\n"
            else:
                # 定义表头
                markdown_result = "| 班级名称 | 课程名称 | 平均分 |\n"
                markdown_result += "|----------|----------|--------|\n"

                # 添加表格内容
                for avg in averages:
                    class_name = avg.get("class_name", "")
                    course_name = avg.get("course_name", "")
                    avg_score = avg.get("avg_score", "")
                    markdown_result += f"| {class_name} | {course_name} | {avg_score} |\n"

            # 返回成功结果
            return {
                "status": "success",
                "message": f"班级平均分获取成功，共{len(averages)}条记录。",
                "data": markdown_result
            }
        else:
            # 返回错误信息
            error_detail = response.json().get("detail", "未知错误")
            return {
                "status": "error",
                "message": f"获取班级平均分失败：{error_detail}",
                "data": None
            }
    except Exception as e:
        # 捕获异常并返回错误信息
        return {
            "status": "error",
            "message": f"请求过程中发生异常：{str(e)}",
            "data": None
        }


def main2222(imagerurl: str, apikey: str) -> dict:
    imagerurl = "![ai](https://sc-maas.oss-cn-shanghai.aliyuncs.com/outputs%2F20250508%2Flv6c9v96wr.jpeg?Expires=1746686984&OSSAccessKeyId=LTAI5tQnPSzwAnR8NmMzoQq4&Signature=I9EFkQuyT14REbApA28x5lwG1%2FQ%3D)"
    # 设置请求的URL和Headers
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "authorization": f"Bearer {apikey}",
        "content-type": "application/json"
    }

    # 添加中文提示词
    prompt_text = "请提取图片信息里面的内容，并使用中文回答。"
    url1 = imagerurl.split('(', 1)[1].split(')', 1)[0]
    payload = {
        "model": "Pro/OpenGVLab/InternVL2-8B",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "text": prompt_text,
                        "image_url": {
                            "url": url1,
                            "detail": "auto"
                        }
                    }
                ]
            }
        ],
        "stream": False,
        "max_tokens": 1024,
        "temperature": 0.3,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"}
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=json.dumps(payload, ensure_ascii=False))

    # 提取结果并返回
    if response.status_code == 200:
        result = response.json()
        # 检查result中是否有choices字段
        if "choices" in result:
            # 获取第一个choice的内容
            content = result["choices"][0]["message"]["content"]
            return {"result": content}
        else:
            return "Error: No choices found in the response."
    else:
        return f"Error: {response.status_code}, {response.text}"


import time

import requests


def main1111(json_html: str, apikey: str, apiurl: str) -> dict:
    try:
        json_html = "<think>\n我需要根据用户提供的电视剧《长安的荔枝》中的五个金句生成一个符合Bento Grid风格的HTML网页。让我分析一下需求和内容：\n\n**内容分析**：\n- 5个电视剧金句，来自《长安的荔枝》\n- 每个金句都有编号和引号\n- 这些金句反映了剧中情节、人物性格，蕴含人生哲理和职场智慧\n\n**设计要求**：\n- Bento Grid风格布局\n- 纯黑色背景和亮橙色作为主要配色\n- 大小字体对比突出核心要点\n- 中英文混用，中文使用大字体粗体，英文小字作为点缀\n- 使用简洁的勾线图形作为数据可视化或配图元素\n- 高亮色自身的透明度渐变制造科技感\n- 类似Apple官网的滚动动效\n- 集成在线图表组件\n- 使用Framer Motion实现动画效果\n- 集成专业图标库(Font Awesome或Material Icons)\n- 优化代码结构和性能\n\n**页面规划**：\n1. 页面标题/头部：展示电视剧名称和简介\n2. Bento Grid布局的金句展示区：每个金句占一个或多个格子\n3. 可能的额外区域：金句分类或主题分析\n4. 页脚：简单信息\n\n让我开始编写HTML代码：\n</think>```html\n<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>长安的荔枝 | 金句集</title>\n    <script src=\"https://cdn.tailwindcss.com\"></script>\n    <link href=\"https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css\" rel=\"stylesheet\">\n    <script src=\"https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js\"></script>\n    <script src=\"https://cdn.jsdelivr.net/npm/framer-motion@10.15.1/dist/framer-motion.min.js\"></script>\n    <script>\n        tailwind.config = {\n            theme: {\n                extend: {\n                    colors: {\n                        primary: '#FF6B00',\n                        dark: '#0A0A0A',\n                        'primary-light': '#FF8A33',\n                        'primary-dark': '#E05A00',\n                    },\n                    fontFamily: {\n                        sans: ['Inter', 'system-ui', 'sans-serif'],\n                    },\n                }\n            }\n        }\n    </script>\n    <style type=\"text/tailwindcss\">\n        @layer utilities {\n            .text-shadow {\n                text-shadow: 0 2px 4px rgba(0,0,0,0.1);\n            }\n            .bento-item {\n                @apply rounded-xl overflow-hidden transition-all duration-500 hover:shadow-lg hover:shadow-primary/20;\n            }\n            .gradient-overlay {\n                background: linear-gradient(135deg, rgba(255,107,0,0.8) 0%, rgba(255,107,0,0.4) 100%);\n            }\n            .scroll-smooth {\n                scroll-behavior: smooth;\n            }\n        }\n    </style>\n</head>\n<body class=\"bg-dark text-white scroll-smooth\">\n    <!-- 导航栏 -->\n    <nav class=\"fixed top-0 left-0 right-0 z-50 bg-dark/80 backdrop-blur-md border-b border-primary/20\">\n        <div class=\"container mx-auto px-4 py-4 flex justify-between items-center\">\n            <div class=\"flex items-center space-x-2\">\n                <i class=\"fa fa-book text-primary text-2xl\"></i>\n                <h1 class=\"text-xl font-bold\">长安的荔枝 <span class=\"text-primary text-sm\">Golden Quotes</span></h1>\n            </div>\n            <div class=\"hidden md:flex space-x-6\">\n                <a href=\"#quotes\" class=\"text-sm hover:text-primary transition-colors\">金句集</a>\n                <a href=\"#themes\" class=\"text-sm hover:text-primary transition-colors\">主题分析</a>\n                <a href=\"#about\" class=\"text-sm hover:text-primary transition-colors\">关于作品</a>\n            </div>\n            <button class=\"md:hidden text-primary\">\n                <i class=\"fa fa-bars text-xl\"></i>\n            </button>\n        </div>\n    </nav>\n\n    <!-- 头部区域 -->\n    <header class=\"pt-32 pb-20 px-4 relative overflow-hidden\">\n        <div class=\"absolute top-0 right-0 w-full h-full bg-primary/5 -skew-y-3 transform origin-top-right\"></div>\n        <div class=\"container mx-auto relative z-10\">\n            <div class=\"max-w-3xl mx-auto text-center\">\n                <h1 class=\"text-[clamp(2rem,5vw,4rem)] font-bold leading-tight mb-6\">\n                    长安的荔枝\n                    <span class=\"block text-primary/80 text-[clamp(1rem,2vw,1.5rem)] font-normal mt-2\">Golden Quotes</span>\n                </h1>\n                <p class=\"text-gray-400 text-lg mb-8 max-w-2xl mx-auto\">\n                    这些金句不仅反映了剧中的情节和人物性格，也蕴含了深刻的人生哲理和职场智慧。\n                </p>\n                <a href=\"#quotes\" class=\"inline-block bg-primary hover:bg-primary-dark text-white font-bold py-3 px-8 rounded-full transition-all transform hover:scale-105\">\n                    探索金句 <i class=\"fa fa-arrow-down ml-2\"></i>\n                </a>\n            </div>\n        </div>\n        \n        <!-- 装饰线条 -->\n        <div class=\"absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent\"></div>\n    </header>\n\n    <!-- 金句Bento Grid区域 -->\n    <section id=\"quotes\" class=\"py-20 px-4\">\n        <div class=\"container mx-auto\">\n            <h2 class=\"text-3xl font-bold mb-12 text-center\">\n                剧中金句 <span class=\"text-primary text-lg\">Famous Lines</span>\n            </h2>\n            \n            <div class=\"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6\">\n                <!-- 金句1 -->\n                <motion.div \n                    class=\"bento-item bg-dark border border-primary/20 p-6 md:col-span-2\"\n                    initial={{ opacity: 0, y: 50 }}\n                    whileInView={{ opacity: 1, y: 0 }}\n                    transition={{ duration: 0.5 }}\n                    viewport={{ once: true }}\n                >\n                    <div class=\"flex items-start\">\n                        <div class=\"text-primary text-4xl font-bold mr-4\">01</div>\n                        <div>\n                            <p class=\"text-xl md:text-2xl font-bold italic mb-4\">\"既是身临绝境，退无可退，何不向前拼死一搏，说不定还能搏出一点微茫希望。\"</p>\n                            <div class=\"flex items-center text-gray-400 text-sm\">\n                                <i class=\"fa fa-lightbulb-o text-primary mr-2\"></i>\n                                <span>绝境求生 · 奋力一搏</span>\n                            </div>\n                        </div>\n                    </div>\n                    <div class=\"mt-6 h-1 w-full bg-gray-800 rounded-full overflow-hidden\">\n                        <div class=\"h-full w-3/4 gradient-overlay\"></div>\n                    </div>\n                </motion.div>\n                \n                <!-- 金句2 -->\n                <motion.div \n                    class=\"bento-item bg-dark border border-primary/20 p-6 flex flex-col justify-center\"\n                    initial={{ opacity: 0, y: 50 }}\n                    whileInView={{ opacity: 1, y: 0 }}\n                    transition={{ duration: 0.5, delay: 0.1 }}\n                    viewport={{ once: true }}\n                >\n                    <div class=\"text-primary text-4xl font-bold mb-4\">02</div>\n                    <p class=\"text-xl font-bold italic mb-6\">\"就算失败，我也想知道，自己倒在距离终点多远的地方。\"</p>\n                    <div class=\"mt-auto flex items-center text-gray-400 text-sm\">\n                        <i class=\"fa fa-flag text-primary mr-2\"></i>\n                        <span>坚持到底 · 自我认知</span>\n                    </div>\n                </motion.div>\n                \n                <!-- 金句3 -->\n                <motion.div \n                    class=\"bento-item bg-dark border border-primary/20 p-6 lg:col-span-2\"\n                    initial={{ opacity: 0, y: 50 }}\n                    whileInView={{ opacity: 1, y: 0 }}\n                    transition={{ duration: 0.5, delay: 0.2 }}\n                    viewport={{ once: true }}\n                >\n                    <div class=\"text-primary text-4xl font-bold mb-4\">03</div>\n                    <p class=\"text-xl md:text-2xl font-bold italic mb-6\">\"做官之道，其实就三句话：和光同尘，雨露均沾，花花轿子众人抬。一个人吃独食，是吃不长久的。\"</p>\n                    <div class=\"flex items-center text-gray-400 text-sm\">\n                        <i class=\"fa fa-balance-scale text-primary mr-2\"></i>\n                        <span>处世哲学 · 职场智慧</span>\n                    </div>\n                </motion.div>\n                \n                <!-- 金句4 -->\n                <motion.div \n                    class=\"bento-item bg-dark border border-primary/20 p-6 flex flex-col justify-center\"\n                    initial={{ opacity: 0, y: 50 }}\n                    whileInView={{ opacity: 1, y: 0 }}\n                    transition={{ duration: 0.5, delay: 0.3 }}\n                    viewport={{ once: true }}\n                >\n                    <div class=\"text-primary text-4xl font-bold mb-4\">04</div>\n                    <p class=\"text-xl font-bold italic mb-6\">\"流程那种东西，是弱者才要遵循的规矩。\"</p>\n                    <div class=\"mt-auto flex items-center text-gray-400 text-sm\">\n                        <i class=\"fa fa-random text-primary mr-2\"></i>\n                        <span>打破常规 · 突破束缚</span>\n                    </div>\n                </motion.div>\n                \n                <!-- 金句5 -->\n                <motion.div \n                    class=\"bento-item bg-dark border border-primary/20 p-6 md:col-span-3\"\n                    initial={{ opacity: 0, y: 50 }}\n                    whileInView={{ opacity: 1, y: 0 }}\n                    transition={{ duration: 0.5, delay: 0.4 }}\n                    viewport={{ once: true }}\n                >\n                    <div class=\"flex flex-col md:flex-row md:items-center\">\n                        <div class=\"text-primary text-4xl font-bold mr-6 mb-4 md:mb-0\">05</div>\n                        <p class=\"text-2xl md:text-3xl font-bold italic\">\"在这个世上，最不能直视的，一是太阳，二是人心。\"</p>\n                    </div>\n                    <div class=\"mt-6 flex items-center text-gray-400 text-sm\">\n                        <i class=\"fa fa-eye-slash text-primary mr-2\"></i>\n                        <span>人性洞察 · 处世箴言</span>\n                    </div>\n                    <div class=\"mt-6 h-1 w-full bg-gray-800 rounded-full overflow-hidden\">\n                        <div class=\"h-full w-5/6 gradient-overlay\"></div>\n                    </div>\n                </motion.div>\n            </div>\n        </div>\n    </section>\n\n    <!-- 主题分析区域 -->\n    <section id=\"themes\" class=\"py-20 px-4 bg-gradient-to-b from-dark to-dark/95\">\n        <div class=\"container mx-auto\">\n            <h2 class=\"text-3xl font-bold mb-12 text-center\">\n                主题分析 <span class=\"text-primary text-lg\">Thematic Analysis</span>\n            </h2>\n            \n            <div class=\"grid grid-cols-1 lg:grid-cols-2 gap-10\">\n                <!-- 图表区域 -->\n                <motion.div \n                    class=\"bento-item bg-dark border border-primary/20 p-6\"\n                    initial={{ opacity: 0, x: -50 }}\n                    whileInView={{ opacity: 1, x: 0 }}\n                    transition={{ duration: 0.5 }}\n                    viewport={{ once: true }}\n                >\n                    <h3 class=\"text-xl font-bold mb-6\">金句主题分布 <span class=\"text-primary text-sm\">Thematic Distribution</span></h3>\n                    <div class=\"h-80\">\n                        <canvas id=\"themeChart\"></canvas>\n                    </div>\n                </motion.div>\n                \n                <!-- 主题描述 -->\n                <motion.div \n                    class=\"flex flex-col justify-center\"\n                    initial={{ opacity: 0, x: 50 }}\n                    whileInView={{ opacity: 1, x: 0 }}\n                    transition={{ duration: 0.5, delay: 0.2 }}\n                    viewport={{ once: true }}\n                >\n                    <div class=\"space-y-6\">\n                        <div class=\"flex items-start\">\n                            <div class=\"w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary mr-4 flex-shrink-0\">\n                                <i class=\"fa fa-briefcase\"></i>\n                            </div>\n                            <div>\n                                <h4 class=\"text-xl font-bold mb-2\">职场智慧</h4>\n                                <p class=\"text-gray-400\">金句中蕴含了丰富的职场生存法则，从团队协作到权力平衡，展现了古代官场与现代职场的共通之处。</p>\n                            </div>\n                        </div>\n                        \n                        <div class=\"flex items-start\">\n                            <div class=\"w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary mr-4 flex-shrink-0\">\n                                <i class=\"fa fa-heart\"></i>\n                            </div>\n                            <div>\n                                <h4 class=\"text-xl font-bold mb-2\">人性洞察</h4>\n                                <p class=\"text-gray-400\">对人心的深刻洞察是金句的重要主题，揭示了人性的复杂与多面，以及在权力面前的真实表现。</p>\n                            </div>\n                        </div>\n                        \n                        <div class=\"flex items-start\">\n                            <div class=\"w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary mr-4 flex-shrink-0\">\n                                <i class=\"fa fa-road\"></i>\n                            </div>\n                            <div>\n                                <h4 class=\"text-xl font-bold mb-2\">人生抉择</h4>\n                                <p class=\"text-gray-400\">面对困境时的抉择与坚持，展现了主人公在绝境中的勇气与智慧，给予观众深刻的人生启示。</p>\n                            </div>\n                        </div>\n                    </div>\n                </motion.div>\n            </div>\n        </div>\n    </section>\n\n    <!-- 关于作品区域 -->\n    <section id=\"about\" class=\"py-20 px-4\">\n        <div class=\"container mx-auto\">\n            <h2 class=\"text-3xl font-bold mb-12 text-center\">\n                关于作品 <span class=\"text-primary text-lg\">About The Work</span>\n            </h2>\n            \n            <div class=\"max-w-4xl mx-auto\">\n                <motion.div \n                    class=\"bento-item bg-dark border border-primary/20 p-8\"\n                    initial={{ opacity: 0, y: 50 }}\n                    whileInView={{ opacity: 1, y: 0 }}\n                    transition={{ duration: 0.5 }}\n                    viewport={{ once: true }}\n                >\n                    <div class=\"flex flex-col md:flex-row gap-8\">\n                        <div class=\"md:w-1/3\">\n                            <div class=\"rounded-xl overflow-hidden border border-primary/30 h-64 md:h-auto\">\n                                <img src=\"https://picsum.photos/id/1067/600/800\" alt=\"长安的荔枝\" class=\"w-full h-full object-cover\">\n                            </div>\n                        </div>\n                        <div class=\"md:w-2/3\">\n                            <h3 class=\"text-2xl font-bold mb-4\">长安的荔枝</h3>\n                            <p class=\"text-gray-300 mb-4\">\n                                《长安的荔枝》是一部以唐朝为背景的历史剧，讲述了主人公在复杂的官场环境中，面对几乎不可能完成的任务，如何凭借智慧与勇气突破重重困难的故事。\n                            </p>\n                            <p class=\"text-gray-300 mb-6\">\n                                剧中的金句不仅反映了主人公的性格成长，也折射出古代官场的生存法则和人性的复杂，给予现代观众深刻的启示与思考。\n                            </p>\n                            <div class=\"grid grid-cols-2 gap-4 text-sm\">\n                                <div class=\"flex items-center\">\n                                    <i class=\"fa fa-tag text-primary mr-2\"></i>\n                                    <span>历史 / 剧情</span>\n                                </div>\n                                <div class=\"flex items-center\">\n                                    <i class=\"fa fa-star text-primary mr-2\"></i>\n                                    <span>评分：9.2/10</span>\n                                </div>\n                                <div class=\"flex items-center\">\n                                    <i class=\"fa fa-calendar text-primary mr-2\"></i>\n                                    <span>2023年播出</span>\n                                </div>\n                                <div class=\"flex items-center\">\n                                    <i class=\"fa fa-trophy text-primary mr-2\"></i>\n                                    <span>多项大奖提名</span>\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n                </motion.div>\n            </div>\n        </div>\n    </section>\n\n    <!-- 页脚 -->\n    <footer class=\"py-10 px-4 border-t border-primary/20\">\n        <div class=\"container mx-auto text-center\">\n            <div class=\"flex justify-center items-center space-x-4 mb-6\">\n                <a href=\"#\" class class"
        apikey = "sk-geekaiapp"
        apiurl = "https://g13.geekaiapp.icu/api/generate-html"
        # 去除输入字符串中的 ```html 和 ``` 标记
        # match = re.search(r'```html\s*([\s\S]*?)```', json_html, re.DOTALL)
        match = re.search(r'```html\s*([\s\S]*?)', json_html, re.DOTALL)

        if match:
            # group(1) 获取第一个捕获组的内容，即纯HTML代码
            # .strip() 去除可能存在的前后空白
            html_content = match.group(1).strip()
        else:
            # 如果在输入中找不到HTML代码块，则返回错误
            raise ValueError("未能在输入中找到 ```html ... ``` 代码块。")

        # 生成时间戳，确保文件名唯一
        timestamp = int(time.time())
        filename = f"makehtml_{timestamp}.html"

        # API端点（假设本地运行）
        url = f"{apiurl}"

        # 请求数据
        payload = {
            "html_content": html_content,
            "filename": filename  # 使用传入的文件名
        }

        # 设置请求头（包含认证token）
        headers = {
            "Authorization": f"Bearer {apikey}",  # 替换为实际的认证token
            "Content-Type": "application/json"
        }

        try:
            # 发送POST请求
            response = requests.post(url, json=payload, headers=headers)

            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                html_url = result.get("html_url", "")
                generated_filename = result.get("filename", "")

                # 返回结果
                return {
                    "html_url": html_url,
                    "filename": generated_filename,
                    "markdown_result": f"[点击查看]({html_url})"
                }
            else:
                raise Exception(f"HTTP Error: {response.status_code}, Message: {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    except Exception as e:
        return {
            "error": f"Error: {str(e)}"
        }


def main2222(arg1: str) -> dict:
    arg1 = "```json\n{\n  \"发票代码\": \"\",\n  \"发票号码\": \"25317000001206184298\",\n  \"开票日期\": \"2025年06月05日\",\n  \"开票类目\": \"食品\",\n  \"金额\": 28.23,\n  \"税额\": 3.68,\n  \"发票类型\": \"增值税电子普通发票\"\n}\n```"
    # 按 ```json 分割，取后半部分
    part = arg1.split('```json', 1)[-1]
    # 再按 ``` 分割，取第一部分并去除首尾空白
    json_content = part.split('```', 1)[0].strip()

    try:
        # 解析JSON内容
        data = json.loads(json_content)
        # 转换为表格格式
        table = []
        for item in data:
            # 为每个发票创建记录，包含所有字段
            invoice_data = [
                item.get('发票代码', ''),
                item.get('发票号码', ''),
                item.get('开票日期', ''),
                item.get('开票类目', ''),
                str(item.get('金额', '')),
                str(item.get('税额', '')),
                item.get('发票类型', '')
            ]
            table.append(invoice_data)

        return {
            "result": str(table).replace("'", '"')
        }
    except json.JSONDecodeError:
        # 若JSON解析失败，返回原始内容
        return {
            "result": [["错误", "JSON解析失败"]]
        }


def main222222(arg1: str) -> dict:
    arg1 = "```json\n{\n  \"发票代码\": \"\",\n  \"发票号码\": \"25317000001206184298\",\n  \"开票日期\": \"2025年06月05日\",\n  \"开票类目\": \"食品\",\n  \"金额\": 28.23,\n  \"税额\": 3.68,\n  \"发票类型\": \"增值税电子普通发票\"\n}\n```"
    # 按 ```json 分割，取后半部分
    part = arg1.split('```json', 1)[-1]
    # 再按 ``` 分割，取第一部分并去除首尾空白
    json_content = part.split('```', 1)[0].strip()

    try:
        # 解析JSON内容
        data = json.loads(json_content)
        # 直接访问字典的字段，不需要遍历
        invoice_data = [
            data.get('发票代码', ''),
            data.get('发票号码', ''),
            data.get('开票日期', ''),
            data.get('开票类目', ''),
            str(data.get('金额', '')),
            str(data.get('税额', '')),
            data.get('发票类型', '')
        ]
        table = [invoice_data]  # 注意：这里用 [] 包裹，因为只有一条记录

        return {
            "result": str(table).replace("'", '"')
        }
    except json.JSONDecodeError:
        # 若JSON解析失败，返回原始内容
        return {
            "result": [["错误", "JSON解析失败"]]
        }


def main(arg1: str) -> dict:
    # 按 ```json 分割，取后半部分
    part = arg1.split('```json', 1)[-1]
    # 再按 ``` 分割，取第一部分并去除首尾空白
    json_content = part.split('```', 1)[0].strip()

    try:
        # 解析JSON内容
        data = json.loads(json_content)
        # 直接访问字典的字段，不需要遍历
        invoice_data = [
            data.get('发票代码', ''),
            data.get('发票号码', ''),
            data.get('开票日期', ''),
            data.get('开票类目', ''),
            str(data.get('金额', '')),
            str(data.get('税额', '')),
            data.get('发票类型', '')
        ]
        table = [invoice_data]  # 注意：这里用 [] 包裹，因为只有一条记录

        return {
            "result": str(table).replace("'", '"')
        }
    except json.JSONDecodeError:
        # 若JSON解析失败，返回原始内容
        return {
            "result": [["错误", "JSON解析失败"]]
        }


def main(arg1: str) -> dict:
    # 按 ```json 分割，取后半部分
    part = arg1.split('```json', 1)[-1]
    # 再按 ``` 分割，取第一部分并去除首尾空白
    json_content = part.split('```', 1)[0].strip()

    try:
        # 解析JSON内容
        data = json.loads(json_content)
        # 转换为表格格式
        table = []
        for item in data:
            # 为每个发票创建记录，包含所有字段
            invoice_data = [
                item.get('发票代码', ''),
                item.get('发票号码', ''),
                item.get('开票日期', ''),
                item.get('开票类目', ''),
                str(item.get('金额', '')),
                str(item.get('税额', '')),
                item.get('发票类型', '')
            ]
            table.append(invoice_data)

        return {
            "result": str(table).replace("'", '"')
        }
    except json.JSONDecodeError:
        # 若JSON解析失败，返回原始内容
        return {
            "result": [["错误", "JSON解析失败"]]
        }


def main11111(arg1: dict) -> dict:
    # 提取输入字典的字段
    question_text = arg1.get("question_text", "")
    subject = arg1.get("subject", "")
    question_type = arg1.get("question_type", "")

    # 确保 difficulty 是字符串类型
    difficulty = arg1.get("difficulty", "")
    if not isinstance(difficulty, str):
        difficulty = str(difficulty)

    answer = arg1.get("answer", "")
    user_answer = arg1.get("user_answer", "")
    explanation = arg1.get("explanation", "")

    # 返回包含所有字段的字典
    return {
        "question_text": question_text.replace("'", "''"),
        "subject": subject.replace("'", "''"),
        "question_type": question_type.replace("'", "''"),
        "difficulty": difficulty.replace("'", "''"),  # 确保此处为字符串
        "answer": answer.replace("'", "''"),
        "user_answer": user_answer.replace("'", "''"),
        "explanation": explanation.replace("'", "''")
    }


def escape_mysql_string(value: any) -> any:
    """转义 MySQL 字符串中的单引号（将 ' 替换为 ''）"""
    if isinstance(value, str):
        return value.replace("'", "''")  # 关键转义逻辑
    return value  # 非字符串类型直接返回


def main1113333(arg1: dict) -> dict:
    # 提取输入字典的字段
    question_text = arg1.get("question_text", "")
    subject = arg1.get("subject", "")
    question_type = arg1.get("question_type", "")

    # 确保 difficulty 是字符串类型（避免数字等非字符串类型）
    difficulty = arg1.get("difficulty", "")
    if not isinstance(difficulty, str):
        difficulty = str(difficulty)

    answer = arg1.get("answer", "")
    user_answer = arg1.get("user_answer", "")
    explanation = arg1.get("explanation", "")

    # 对所有字符串字段进行转义处理（替换 ' 为 ''）
    return {
        "question_text": escape_mysql_string(question_text),
        "subject": escape_mysql_string(subject),
        "question_type": escape_mysql_string(question_type),
        "difficulty": escape_mysql_string(difficulty),  # 已确保是字符串，直接转义
        "answer": escape_mysql_string(answer),
        "user_answer": escape_mysql_string(user_answer),
        "explanation": escape_mysql_string(explanation)
    }


def main22212(markdown_table: str) -> dict:
    markdown_table = "question_text                           |subject|question_type|created_at         \n----------------------------------------|-------|-------------|-------------------\nDaming is going to learn how to _______.|英语     |选择题          |2025-07-30T14:10:11"
    try:
        # 去除首尾空白，分割每一行
        lines = markdown_table.strip().split('\n')

        # 提取表头
        headers = [h.strip() for h in lines[0].split('|')]

        # 获取 question_text 所在列索引
        try:
            question_index = headers.index('question_text')
            question_type_index = headers.index('question_type')
        except ValueError:
            return {"error": "缺少 question_text或question_type 列"}

        # 提取 question_text 内容
        questions = []
        for line in lines[2:]:  # 跳过表头和分隔线
            if not line.strip():
                continue
            columns = [col.strip() for col in line.split('|')]
            if len(columns) > question_index:
                questions.append(columns[question_type_index] + ':' + columns[question_index])

        return {"error_questions": questions}

    except Exception as e:
        return {"error": f"发生错误: {str(e)}"}


# def main(markdown_table: str) -> dict:
#     try:
#         # 去除首尾空白，分割每一行
#         lines = markdown_table.strip().split('\n')
#
#         # 提取表头
#         headers = [h.strip() for h in lines[0].split('|')]
#
#         # 获取 question_text 所在列索引
#         try:
#             question_index = headers.index('question_text')
#             question_type_index = headers.index('question_type')
#         except ValueError:
#             return {"error": "缺少 question_text或question_type 列"}
#
#         # 提取 question_text 内容
#         questions = []
#         for line in lines[2:]:  # 跳过表头和分隔线
#             if not line.strip():
#                 continue
#             columns = [col.strip() for col in line.split('|')]
#             if len(columns) > question_index:
#                 questions.append(columns[question_type_index]+':'+columns[question_index])
#
#         return {"error_questions": questions}
#
#     except Exception as e:
#         return {"error": f"发生错误: {str(e)}"}


def main1321(markdown_table: str) -> dict:
    try:
        # 去除首尾空白，分割每一行
        lines = markdown_table.strip().split('\n')

        # 提取表头
        headers = [h.strip() for h in lines[0].split('|')]

        # 获取 question_text 所在列索引
        try:
            question_index = headers.index('question_text')
        except ValueError:
            return {"error": "缺少 question_text 列"}

        # 提取 question_text 内容
        questions = []
        for line in lines[2:]:  # 跳过表头和分隔线
            if not line.strip():
                continue
            columns = [col.strip() for col in line.split('|')]
            if len(columns) > question_index:
                questions.append(columns[question_index])

        return {"error_questions": questions}

    except Exception as e:
        return {"error": f"发生错误: {str(e)}"}


def main432(arg1: str) -> dict:
    arg1 = "```json\n{\n  \"original_question\": \"根据短文内容，填空。（每空一词）\\n1. Daming can learn to ______ ______ himself by doing housework.\\n2. The ______ holiday is coming.\\n3. Daming's parents will be happy to enjoy the ______.\\n\\n二、根据短文内容，选择正确答案。\\n1. Daming often does housework, such as ______.\\n   A. watering trees B. mopping the floor C. washing clothes\\n2. Cleaning rooms and ______ can make our house clean and tidy.\\n   A. desks B. windows C. computers\\n3. Daming is going to learn how to ______.\\n   A. cook B. clean C. wash\",\n  \"generated_questions\": [\n    {\n      \"question_text\": \"根据短文内容，填空。（每空一词）\\n1. Xiaoming can learn to ______ ______ himself by doing housework.\\n2. The ______ holiday is coming.\\n3. Xiaoming's parents will be happy to enjoy the ______.\\n\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"2\",\n      \"answer\": \"look after; summer; dishes\",\n      \"explanation\": \"根据短文内容，填空。每空一词。\\n1. 从原文可知，Daming通过做家务可以学会照顾自己，因此填入‘look after’。\\n2. 夏天的假期即将到来，因此填入‘summer’。\\n3. Daming的父母会很高兴享受这些菜肴，因此填入‘dishes’。\"\n    },\n    {\n      \"question_text\": \"根据短文内容，选择正确答案。\\n1. Xiaoming often does housework, such as ______.\\n   A. sweeping the floor B. planting flowers C. washing clothes\\n2. Cleaning rooms and ______ can make our house clean and tidy.\\n   A. tables B. windows C. sofas\\n3. Xiaoming is going to learn how to ______.\\n   A. cook B. clean C. water plants\",\n      \"question_type\": \"选择题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"2\",\n      \"answer\": \"CBA\",\n      \"explanation\": \"根据短文内容，选择正确答案。\\n1. 从原文可知，Daming经常做家务，比如洗衣服，因此选‘washing clothes’。\\n2. 清洁房间和窗户可以让我们的房子干净整洁，因此选‘windows’。\\n3. Xiaoming打算学习如何做饭，因此选‘cook’。\"\n    },\n    {\n      \"question_text\": \"根据短文内容，填空。（每空一词）\\n1. Lily can learn to ______ ______ herself by doing housework.\\n2. The ______ holiday is coming.\\n3. Lily's parents will be happy to enjoy the ______.\\n\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"2\",\n      \"answer\": \"take care; winter; cakes\",\n      \"explanation\": \"根据短文内容，填空。每空一词。\\n1. 从原文可知，Lily通过做家务可以学会照顾自己，因此填入‘take care’。\\n2. 冬天的假期即将到来，因此填入‘winter’。\\n3. Lily的父母会很高兴享受这些蛋糕，因此填入‘cakes’。\"\n    },\n    {\n      \"question_text\": \"根据短文内容，选择正确答案。\\n1. Lily often does housework, such as ______.\\n   A. sweeping the floor B. planting vegetables C. washing dishes\\n2. Cleaning rooms and ______ can make our house clean and tidy.\\n   A. chairs B. doors C. lamps\\n3. Lily is going to learn how to ______.\\n   A. sew B. clean C. bake\",\n      \"question_type\": \"选择题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"2\",\n      \"answer\": \"CBC\",\n      \"explanation\": \"根据短文内容，选择正确答案。\\n1. 从原文可知，Lily经常做家务，比如洗碗，因此选‘washing dishes’。\\n2. 清洁房间和椅子可以让我们的房子干净整洁，因此选‘chairs’。\\n3. Lily打算学习如何烘焙，因此选‘bake’。\"\n    },\n    {\n      \"question_text\": \"根据短文内容，填空。（每空一词）\\n1. Tom can learn to ______ ______ himself by doing housework.\\n2. The ______ holiday is coming.\\n3. Tom's parents will be happy to enjoy the ______.\\n\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"2\",\n      \"answer\": \"take care; spring; cookies\",\n      \"explanation\": \"根据短文内容，填空。每空一词。\\n1. 从原文可知，Tom通过做家务可以学会照顾自己，因此填入‘take care’。\\n2. 春天的假期即将到来，因此填入‘spring’。\\n3. Tom的父母会很高兴享受这些饼干，因此填入‘cookies’。\"\n    },\n    {\n      \"question_text\": \"根据短文内容，选择正确答案。\\n1. Tom often does housework, such as ______.\\n   A. watering plants B. sweeping the floor C. ironing clothes\\n2. Cleaning rooms and ______ can make our house clean and tidy.\\n   A. beds B. mirrors C. refrigerators\\n3. Tom is going to learn how to ______.\\n   A. paint B. clean C. fold laundry\",\n      \"question_type\": \"选择题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"2\",\n      \"answer\": \"ABC\",\n      \"explanation\": \"根据短文内容，选择正确答案。\\n1. 从原文可知，Tom经常做家务，比如扫地，因此选‘sweeping the floor’。\\n2. 清洁房间和床可以让我们的房子干净整洁，因此选‘beds’。\\n3. Tom打算学习如何熨衣服，因此选‘ironing clothes’。\"\n    }\n  ]\n}\n```"
    try:
        # 移除可能存在的Markdown代码块标记
        cleaned_json = arg1.strip()
        if cleaned_json.startswith('```json'):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.endswith('```'):
            cleaned_json = cleaned_json[:-3]
        print(cleaned_json)  # 👈 先打印出来看看长什么样！
        # 处理转义字符，并确保正确的编码处理
        # cleaned_json = cleaned_json.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
        # **替换转义符**：将 \\n 转为 \n（适用于 JSON 中用双反斜杠表示换行的场景）
        cleaned_json = cleaned_json.replace('\\\\n', '\\n')  # 将四个反斜杠转为两个（JSON 标准转义）
        print(cleaned_json)  # 👈 先打印出来看看长什么样！
        # 将 JSON 字符串解析为 Python 字典
        result_dict = json.loads(cleaned_json)
        return {"result": result_dict}  # 返回解析结果
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}"}
    except Exception as e:
        return {"error": f"发生未知错误: {e}"}


def main(arg1: str) -> dict:
    try:
        cleaned_json = arg1.strip()
        if cleaned_json.startswith('```json'):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.endswith('```'):
            cleaned_json = cleaned_json[:-3]
        print(cleaned_json)  # 👈 先打印出来看看长什么样！
        # 处理转义字符，并确保正确的编码处理
        # cleaned_json = cleaned_json.encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')
        # **替换转义符**：将 \\n 转为 \n（适用于 JSON 中用双反斜杠表示换行的场景）
        cleaned_json = cleaned_json.replace('\\\\n', '\\n')  # 将四个反斜杠转为两个（JSON 标准转义）
        print(cleaned_json)  # 👈 先打印出来看看长什么样！
        # 将 JSON 字符串解析为 Python 字典
        result_dict = json.loads(cleaned_json)
        return {"result": result_dict}  # 返回解析结果
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}"}
    except Exception as e:
        return {"error": f"发生未知错误: {e}"}


def main234(arg1) -> dict:
    try:
        # 检查arg1的类型，如果已经是列表，直接使用；如果是字符串，尝试解析JSON
        if isinstance(arg1, list):
            markdown_json_list = arg1
        elif isinstance(arg1, str):
            # 尝试解析为JSON对象
            outer_dict = json.loads(arg1)
            markdown_json_list = outer_dict.get("arg1", [])
        elif isinstance(arg1, dict):
            # 如果是字典，直接获取arg1字段
            markdown_json_list = arg1.get("arg1", [])
        else:
            # 不支持的类型
            return {"markdown_text": f"输入类型不支持：{type(arg1)}"}

        markdown_text = ""
        original_questions_processed = {}
        question_counter = {}

        for markdown_json_str in markdown_json_list:
            # 提取内层JSON字符串（去除```json和```标记）
            match = re.search(r'```json\s*(.*?)\s*```', markdown_json_str, re.DOTALL)
            if not match:
                continue
            inner_json_str = match.group(1).strip()

            try:
                # 解析内层JSON数据
                question_data = json.loads(inner_json_str)
                original_question = question_data.get("original_question", "")
                generated_questions = question_data.get("generated_questions", [])

                # 为每个原题分配一个编号
                if original_question not in original_questions_processed:
                    original_questions_processed[original_question] = len(original_questions_processed) + 1
                    question_counter[original_question] = 0

                original_question_num = original_questions_processed[original_question]

                # 只有第一次遇到原题时才添加原题信息
                if question_counter[original_question] == 0:
                    markdown_text += f"## 原题{original_question_num}：{original_question}\n\n"

                for i, question in enumerate(generated_questions, 1):
                    # 更新同类型题的计数
                    question_counter[original_question] += 1
                    current_question_num = question_counter[original_question]

                    # 处理转义换行符（将JSON中的\n转换为实际换行）
                    explanation = question.get("explanation", "").replace("\\n", "\n")

                    # 如果不是第一个同类型题，再次显示原题信息
                    if i > 1 or current_question_num > 1:
                        markdown_text += f"## 原题{original_question_num}：{original_question}\n\n"

                    markdown_text += f"### 同类型题{current_question_num}：{question.get('question_text', '')}\n\n"
                    markdown_text += f"**题目类型**：{question.get('question_type', '')}\n\n"
                    markdown_text += f"**学科**：{question.get('subject', '')}\n\n"
                    markdown_text += f"**难度等级(1-5)**：{question.get('difficulty_level', '')}\n\n"
                    markdown_text += f"**题目答案**：{question.get('answer', '')}\n\n"
                    markdown_text += f"**题目详解**：\n\n{explanation}\n\n---\n\n"
            except json.JSONDecodeError:
                continue

        return {"markdown_text": markdown_text}
    except Exception as e:
        return {"markdown_text": f"处理过程中出错：{str(e)}"}


def main(arg1: str) -> dict:
    try:
        # 移除可能存在的Markdown代码块标记
        cleaned_json = arg1.strip()
        if cleaned_json.startswith('```json'):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.endswith('```'):
            cleaned_json = cleaned_json[:-3]
        print(cleaned_json)  # 👈 先打印出来看看长什么样！
        cleaned_json = cleaned_json.replace('\\\\n', '\\n')  # 将四个反斜杠转为两个（JSON 标准转义）
        print(cleaned_json)  # 👈 先打印出来看看长什么样！
        # 将 JSON 字符串解析为 Python 字典
        result_dict = json.loads(cleaned_json)
        bean1 = arg1.get("arg1", {})
        bean12 = bean1.get("original_question", {})
        markdown_json_list = bean1.get("generated_questions", [])
        markdown_text = ""
        original_questions_processed = {}
        question_counter = {}

        for markdown_json_str in markdown_json_list:
            # 提取内层JSON字符串（去除```json和```标记）
            match = re.search(r'```json\s*(.*?)\s*```', markdown_json_str, re.DOTALL)
            if not match:
                continue
            inner_json_str = match.group(1).strip()

            try:
                # 解析内层JSON数据
                question_data = json.loads(inner_json_str)
                original_question = question_data.get("original_question", "")
                generated_questions = question_data.get("generated_questions", [])

                # 为每个原题分配一个编号
                if original_question not in original_questions_processed:
                    original_questions_processed[original_question] = len(original_questions_processed) + 1
                    question_counter[original_question] = 0

                original_question_num = original_questions_processed[original_question]

                # 只有第一次遇到原题时才添加原题信息
                if question_counter[original_question] == 0:
                    markdown_text += f"## 原题{original_question_num}：{original_question}\n\n"

                for i, question in enumerate(generated_questions, 1):
                    # 更新同类型题的计数
                    question_counter[original_question] += 1
                    current_question_num = question_counter[original_question]

                    # 处理转义换行符（将JSON中的\n转换为实际换行）
                    explanation = question.get("explanation", "").replace("\\n", "\n")

                    # 如果不是第一个同类型题，再次显示原题信息
                    if i > 1 or current_question_num > 1:
                        markdown_text += f"## 原题{original_question_num}：{original_question}\n\n"

                    markdown_text += f"### 同类型题{current_question_num}：{question.get('question_text', '')}\n\n"
                    markdown_text += f"**题目类型**：{question.get('question_type', '')}\n\n"
                    markdown_text += f"**学科**：{question.get('subject', '')}\n\n"
                    markdown_text += f"**难度等级(1-5)**：{question.get('difficulty_level', '')}\n\n"
                    markdown_text += f"**题目答案**：{question.get('answer', '')}\n\n"
                    markdown_text += f"**题目详解**：\n\n{explanation}\n\n---\n\n"
            except json.JSONDecodeError:
                continue

        return {"markdown_text": markdown_text}
    except Exception as e:
        return {"markdown_text": f"处理过程中出错：{str(e)}"}


import json
import re


def main2254(arg1: str) -> dict:
    arg1 = "```json\n{\n  \"original_question\": \"用所给单词的适当形式填空。\\n[1] He ____ (watch) TV too often.\\n[2] I like ____ (dance).\\n[3] All the girls are ____ (play) volleyball.\",\n  \"generated_questions\": [\n    {\n      \"question_text\": \"用所给单词的适当形式填空。\\n[1] She ____ (read) books every day.\\n[2] They enjoy ____ (sing) songs together.\\n[3] The children are ____ (run) in the park.\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"3\",\n      \"answer\": \"reads, singing, running\",\n      \"explanation\": \"在这些题目中，我们需要根据句子的时态和主语的人称来选择正确的动词形式。例如，在第一个句子中，由于主语是第三人称单数She，并且描述的是日常习惯，所以使用动词的单三形式reads。第二个句子中，like后面接动词的ing形式，因此填singing。第三个句子中，be动词are后面接动词的现在分词形式，因此填running。\"\n    },\n    {\n      \"question_text\": \"用所给单词的适当形式填空。\\n[1] He ____ (study) hard at school.\\n[2] We prefer ____ (swim) in the sea.\\n[3] The students are ____ (write) reports.\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"3\",\n      \"answer\": \"studies, swimming, writing\",\n      \"explanation\": \"在这些题目中，我们需要根据句子的时态和主语的人称来选择正确的动词形式。例如，在第一个句子中，由于主语是第三人称单数He，并且描述的是常态行为，所以使用动词的单三形式studies。第二个句子中，prefer后面接动词的ing形式，因此填swimming。第三个句子中，be动词are后面接动词的现在分词形式，因此填writing。\"\n    },\n    {\n      \"question_text\": \"用所给单词的适当形式填空。\\n[1] They ____ (live) in a big city.\\n[2] My sister likes ____ (cook) meals.\\n[3] The boys are ____ (play) football.\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"3\",\n      \"answer\": \"live, cooking, playing\",\n      \"explanation\": \"在这些题目中，我们需要根据句子的时态和主语的人称来选择正确的动词形式。例如，在第一个句子中，由于主语是复数They，并且描述的是常态行为，所以使用动词原形live。第二个句子中，like后面接动词的ing形式，因此填cooking。第三个句子中，be动词are后面接动词的现在分词形式，因此填playing。\"\n    },\n    {\n      \"question_text\": \"用所给单词的适当形式填空。\\n[1] She ____ (work) in an office.\\n[2] They enjoy ____ (travel) around the world.\\n[3] The children are ____ (draw) pictures.\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"3\",\n      \"answer\": \"works, traveling, drawing\",\n      \"explanation\": \"在这些题目中，我们需要根据句子的时态和主语的人称来选择正确的动词形式。例如，在第一个句子中，由于主语是第三人称单数She，并且描述的是常态行为，所以使用动词的单三形式works。第二个句子中，enjoy后面接动词的ing形式，因此填traveling。第三个句子中，be动词are后面接动词的现在分词形式，因此填drawing。\"\n    },\n    {\n      \"question_text\": \"用所给单词的适当形式填空。\\n[1] He ____ (sleep) late last night.\\n[2] We like ____ (read) books.\\n[3] The students are ____ (listen) to music.\",\n      \"question_type\": \"填空题\",\n      \"subject\": \"英语\",\n      \"difficulty_level\": \"3\",\n      \"answer\": \"slept, reading, listening\",\n      \"explanation\": \"在这些题目中，我们需要根据句子的时态和主语的人称来选择正确的动词形式。例如，在第一个句子中，由于last night表示过去的时间，所以使用动词的一般过去式slept。第二个句子中，like后面接动词的ing形式，因此填reading。第三个句子中，be动词are后面接动词的现在分词形式，因此填listening。\"\n    }\n  ]\n}\n```"
    try:
        match = re.search(r'```json\s*(.*?)\s*```', arg1, re.DOTALL)
        inner_json_str = match.group(1).strip()
        markdown_text1 = ""
        markdown_text = ""
        original_questions_processed = {}
        question_counter = {}
        try:
            question_data = json.loads(inner_json_str)
            original_question = question_data.get("original_question", "")
            generated_questions = question_data.get("generated_questions", [])
            # 为每个原题分配一个编号
            if original_question not in original_questions_processed:
                original_questions_processed[original_question] = len(original_questions_processed) + 1
                question_counter[original_question] = 0

            original_question_num = original_questions_processed[original_question]

            # 只有第一次遇到原题时才添加原题信息
            if question_counter[original_question] == 0:
                markdown_text1 = f"## 原题{original_question_num}：{original_question}\n\n"

            for i, question in enumerate(generated_questions, 1):
                # 更新同类型题的计数
                question_counter[original_question] += 1
                current_question_num = question_counter[original_question]

                # 处理转义换行符（将JSON中的\n转换为实际换行）
                explanation = question.get("explanation", "").replace("\\n", "\n")

                # # 如果不是第一个同类型题，再次显示原题信息
                # if i > 1 or current_question_num > 1:
                #     markdown_text1 = f"## 原题{original_question_num}：{original_question}\n\n"

                markdown_text += f"### 同类型题{current_question_num}：{question.get('question_text', '')}\n\n"
                markdown_text += f"**题目类型**：{question.get('question_type', '')}\n\n"
                markdown_text += f"**学科**：{question.get('subject', '')}\n\n"
                markdown_text += f"**难度等级(1-5)**：{question.get('difficulty_level', '')}\n\n"
                markdown_text += f"**题目答案**：{question.get('answer', '')}\n\n"
                markdown_text += f"**题目详解**：\n\n{explanation}\n\n---\n\n"
        except Exception as e:
            return {"error": f"发生未知错误: {e}"}
        return {"markdown_text": markdown_text1 + markdown_text}
    except Exception as e:
        return {"markdown_text": f"处理过程中出错：{str(e)}"}

import re
import json
def main1222(body: str) -> dict:
    match = re.search(r'```json\s*(.*?)\s*```', body, re.DOTALL)
    if not match:
        return {"error": "未找到有效的 JSON 数据块（需以 ```json 开头和 ``` 结尾）"}
    try:
        json_str = match.group(1)
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败。错误信息: {str(e)}"}
    except Exception as e:
        return {"error": f"其他错误: {str(e)}"}
    if not isinstance(data, dict):
        return {"error": "解析后的 JSON 内容不是对象类型"}
    print("解析后的数据结构（缩进显示）：")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"result": data}

if __name__ == "__main__":
    # main2222("http://127.0.0.1:9090","sk-mcqzdkchqbmrctzsldzjdoplcsnsqovbetjfwvkfaolalowr")
    # main1111('','','')
    # main2222("")
    # main222222("")
    # main22212("")
    # main2254("")
    main1222("")
