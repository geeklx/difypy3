import json
from typing import List

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()

from openai import OpenAI

client = OpenAI(
    # api_key="sk-53e19b5b47db4194912d1c254ecc3d43",
    api_key="sk-c59a31cce2c442eaa7fae4790182b5b3",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # base_url="https://api.deepseek.com",
)

# model1 = "deepseek-chat"
model1 = "qwen-max"

# 定义请求体模型
input1: str = "你是一位英语教学专家，请根据用户将提供给你的内容，请你分析内容，并提取其中的关键信息，识别出中文对应的英文写错的部分,以 JSON 的形式输出，输出的 JSON 需遵守以下的格式：{\"errors\":[{\"序号\":<1>,\"汉语\":<n.保证(书),保修单vt.保证,提供(产品)保修单>,\"错误英语\":<gooe>,\"正确英语\":<gruarantee>}]}"
input: str = "{\"content\":[{\"序号\":1,\"汉语\":\"n.哨兵 n./vt.守卫,保卫,看守\",\"英语\":\"guard\"},{\"序号\":2,\"汉语\":\"vt.保护,护卫 n.安全装置\",\"英语\":\"safeguard\"},{\"序号\":3,\"汉语\":\"vt.认为,注视 n.注意,尊重,问候\",\"英语\":\"regard\"},{\"序号\":4,\"汉语\":\"prep.关于\",\"英语\":\"regarding\"},{\"序号\":5,\"汉语\":\"ad.不顾后果地,不管怎样\",\"英语\":\"regardless\"},{\"序号\":6,\"汉语\":\"n.监护人,守卫者,保护者\",\"英语\":\"guardian\"},{\"序号\":7,\"汉语\":\"n.被监护人,病房,行政区 v.防止\",\"英语\":\"ward\"},{\"序号\":8,\"汉语\":\"n.奖品,奖学金,授予 vt.授予,判给\",\"英语\":\"award\"},{\"序号\":9,\"汉语\":\"n.报酬,奖赏 vt.奖励,奖赏,报答\",\"英语\":\"reward\"},{\"序号\":10,\"汉语\":\"n.保证(书),保修单 vt.保证,提供(产品)保修单\",\"英语\":\"quarter\"},{\"序号\":11,\"汉语\":\"vt.保证 n.令状,凭单,正当理由\",\"英语\":\"warrant\"},{\"序号\":12,\"汉语\":\"n.盒,箱,容器\",\"英语\":\"case\"},{\"序号\":13,\"汉语\":\"n.现金,现款 vt.兑现,付(或收)现款\",\"英语\":\"cash\"},{\"序号\":14,\"汉语\":\"n.收银员,出纳员\",\"英语\":\"cashier\"},{\"序号\":15,\"汉语\":\"n.盒式磁带\",\"英语\":\"cassette\"},{\"序号\":16,\"汉语\":\"n.事例,情形,论据,调查的条件\",\"英语\":\"case\"},{\"序号\":17,\"汉语\":\"a.偶然的,非正式的,临时的,不在乎的\",\"英语\":\"casual\"},{\"序号\":18,\"汉语\":\"n.伤亡人员,受害人,牺牲品\",\"英语\":\"casualty\"},{\"序号\":19,\"汉语\":\"n.场合,时刻,时机,机会\",\"英语\":\"occasion\"},{\"序号\":20,\"汉语\":\"v.接待,尽职责,发(球) vt.适合,供应 vt.可用作,可当……使\",\"英语\":\"serve\"},{\"序号\":21,\"汉语\":\"v.应受(奖赏或惩罚),值得\",\"英语\":\"deserve\"},{\"序号\":22,\"汉语\":\"n.仆人\",\"英语\":\"servant\"},{\"序号\":23,\"汉语\":\"vt.动物等(保护);(水等能源)节约\",\"英语\":\"reserve\"},{\"序号\":24,\"汉语\":\"vt.保护,维护,保留,保存 n.(某群体独有的活动,果酱,腌菜)\",\"英语\":\"preserve\"},{\"序号\":25,\"汉语\":\"vt.保留,预订 n.储备(物);(英)(野生生物)保护区\",\"英语\":\"reserve\"},{\"序号\":26,\"汉语\":\"n.保存,保护\",\"英语\":\"conservation\"},{\"序号\":27,\"汉语\":\"a.保守的 n.保守主义者,保守党党员\",\"英语\":\"conservative\"},{\"序号\":28,\"汉语\":\"n.储藏,保存\",\"英语\":\"preservation\"},{\"序号\":29,\"汉语\":\"n.保留,保留意见,预订\",\"英语\":\"reservation\"},{\"序号\":30,\"汉语\":\"n.水库,蓄水池\",\"英语\":\"reservoir\"},{\"序号\":31,\"汉语\":\"vt.观察,评论,遵守,奉行\",\"英语\":\"observe\"},{\"序号\":32,\"汉语\":\"n.观察,观察结果,评论\",\"英语\":\"observation\"},{\"序号\":33,\"汉语\":\"n.观察者,观察员\",\"英语\":\"observer\"},{\"序号\":34,\"汉语\":\"n.线条,带状物,条纹\",\"英语\":\"stripe\"},{\"序号\":35,\"汉语\":\"n.带子 vt.捆扎,包扎\",\"英语\":\"strap\"},{\"序号\":36,\"汉语\":\"n.条,带\",\"英语\":\"strip\"},{\"序号\":37,\"汉语\":\"vt.剥,剥去; (of)剥夺,夺走\",\"英语\":\"strip\"},{\"序号\":38,\"汉语\":\"a.特殊的,有专门作用的,格外的\",\"英语\":\"special\"},{\"序号\":39,\"汉语\":\"ad.专门地,特意,格外,尤其\",\"英语\":\"specially\"},{\"序号\":40,\"汉语\":\"ad.专门,特地,特别,尤其\",\"英语\":\"especially\"},{\"序号\":41,\"汉语\":\"n.专家\",\"英语\":\"specialist\"},{\"序号\":42,\"汉语\":\"vt.专门研究,专门从事,专攻\",\"英语\":\"specialise\"},{\"序号\":43,\"汉语\":\"n.专业,专长,特色食品\",\"英语\":\"specialty\"},{\"序号\":44,\"汉语\":\"a.特有的,具体的 n.(pl.)细节\",\"英语\":\"specific\"},{\"序号\":45,\"汉语\":\"ad.特意地,专门地,明确地\",\"英语\":\"specifically\"},{\"序号\":46,\"汉语\":\"vt.具体指明,详细说明\",\"英语\":\"specify\"},{\"序号\":47,\"汉语\":\"n.详述;(常 pl.)规格,说明书\",\"英语\":\"specification\"},{\"序号\":48,\"汉语\":\"n.物种,种类\",\"英语\":\"species\"},{\"序号\":49,\"汉语\":\"n.标本,样品,样本,实例,范例\",\"英语\":\"specimen\"},{\"序号\":50,\"汉语\":\"n.面纱,遮蔽物 vt.掩饰;[文]遮掩\",\"英语\":\"veil\"}]}"

params = [
    {
        "role": "system",
        "content": input1
    },
    {
        "role": "user",
        "content": input
    }
]


@app.post("/dps1/")
async def get_dps1():
    try:
        response = client.chat.completions.create(
            model=model1,
            messages=params,
            response_format={
                'type': 'json_object'
            }
        )

        print(response.choices[0].message.content)
        return {
            "你的错误": json.loads(response.choices[0].message.content)
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class Item(BaseModel):
    role: str
    content: str


class TxtRequest(BaseModel):
    messages: List[Item] = [
        {
            "role": "system",
            "content": input1
        },
        {
            "role": "user",
            "content": input
        }
    ]


system_prompt = """
你是一位英语教学专家，请根据用户将提供给你的内容，请你分析内容，并提取其中的关键信息，识别出中文对应的英文写错的部分,以 JSON 的形式输出，输出的 JSON 需遵守以下的格式：

示例输入: 
{
    "content": [
        {
            "序号": 1,
            "汉语": "n.哨兵 n./vt.守卫,保卫,看守",
            "英语": "guard"
        },
        {
            "序号": 2,
            "汉语": "vt.保护,护卫 n.安全装置",
            "英语": "safeguard"
        }
    ]
}

JSON 输出示例:
{
  "errors": [
    {
      "序号": <1>,
      "汉语": <n.保证(书),保修单 vt.保证,提供(产品)保修单>,
      "错误英语": <gooe>,
      "正确英语": <gruarantee>
    }
  ]
}
"""

user_prompt = "{\"content\":[{\"序号\":1,\"汉语\":\"n.哨兵 n./vt.守卫,保卫,看守\",\"英语\":\"guard\"},{\"序号\":9,\"汉语\":\"n.报酬,奖赏 vt.奖励,奖赏,报答\",\"英语\":\"reward\"},{\"序号\":10,\"汉语\":\"n.保证(书),保修单 vt.保证,提供(产品)保修单\",\"英语\":\"quarter\"},{\"序号\":11,\"汉语\":\"vt.保证 n.令状,凭单,正当理由\",\"英语\":\"warrant\"},{\"序号\":50,\"汉语\":\"n.面纱,遮蔽物 vt.掩饰;[文]遮掩\",\"英语\":\"veila\"}]}"

user_prompt2 = """
    {
  "content": [
    {
      "序号": 1,
      "汉语": "n.哨兵 n./vt.守卫,保卫,看守",
      "英语": "guard"
    },
    {
      "序号": 9,
      "汉语": "n.报酬,奖赏 vt.奖励,奖赏,报答",
      "英语": "reward"
    },
    {
      "序号": 10,
      "汉语": "n.保证(书),保修单 vt.保证,提供(产品)保修单",
      "英语": "quarter"
    },
    {
      "序号": 11,
      "汉语": "vt.保证 n.令状,凭单,正当理由",
      "英语": "warrant"
    },
    {
      "序号": 50,
      "汉语": "n.面纱,遮蔽物 vt.掩饰;[文]遮掩",
      "英语": "veila"
    }
  ]
}    
"""

messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]


@app.post("/dps12/")
async def get_dps12(sys_pt1: str, user_pt1: str):
    try:
        response = client.chat.completions.create(
            model=model1,
            # messages=messages,
            messages=[
                {
                    "role": "system",
                    "content": sys_pt1
                },
                {
                    "role": "user",
                    "content": user_pt1
                }
            ],
            response_format={
                'type': 'json_object'
            }
        )
        print(json.loads(response.choices[0].message.content))
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dps123/")
async def get_dps123(request: Request):
    try:
        data = await request.json()
        # print(f'data ={data}')
        text = data.get('content')
        # print(f'text ={text}')
        response = client.chat.completions.create(
            model=model1,
            # messages=messages,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(text, ensure_ascii=False)
                }
            ],
            response_format={
                'type': 'json_object'
            }
        )
        print(json.loads(response.choices[0].message.content))
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5058)
