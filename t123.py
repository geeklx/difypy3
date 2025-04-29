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


import requests


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


if __name__ == "__main__":
    main111("http://127.0.0.1:9090")
