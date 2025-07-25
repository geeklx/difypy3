import asyncio
import json
import os

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

browser = Browser(
    config=BrowserConfig(
        headless=True,
        new_context_config=BrowserContextConfig(
            viewport_expansion=0,
        )
    )
)

# 还有十块
llm = ChatOpenAI(
    base_url='https://api.deepseek.com/v1',
    model='deepseek-chat',
    api_key=SecretStr('sk-b74d50f76da04c4aaae418b3c2c576d5'),
)

# 没钱了
llm2 = ChatOpenAI(
    base_url='https://api.302.ai/v1',
    model='gemini-2.5-flash-preview-05-20',
    api_key=SecretStr('XXXXXXXXXX'),
)

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# config = BrowserConfig(
#     headless=False,
#     disable_security=True
# )

browser1 = Browser(
    config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            viewport_expansion=0,
        )
    )
)

# browser2 = Browser(
#     config=BrowserConfig(
#         browser_instance_path=CHROME_PATH,
#         new_context_config=BrowserContextConfig(
#             _force_keep_context_alive=True,
#         ),
#     ),
# )

file_path = os.path.join(os.path.dirname(__file__), 'taobao_cookies.json')
context = BrowserContext(browser=browser, config=BrowserContextConfig(cookies_file=file_path))


async def run_search():
    agent2 = Agent(
        task="""
             1.打开https://www.taobao.com/，等待页面加载完毕，
             2.新页面加载完毕后，如果出现弹出窗，请关闭，
             3.页面中检测到购物车相关的内容，就点击购物车，进入我的购物车新页面，
             4.收集我的购物车页面中全部商品下面的列表信息，
             5.最后输出数据的格式为json格式，
             6.完成.
         		""",
        llm=llm,
        use_vision=False,
        max_actions_per_step=4,
        browser_context=context,
    )
    # await agent.run(max_steps=25)
    result = await agent2.run()
    final_output = result.final_result()
    if final_output is not None and '```json' in final_output:
        try:
            part = final_output.split('```json', 1)[-1]
            json_content = part.split('```', 1)[0].strip()
            data = json.loads(json_content)
            with open('Gemini.md', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {
                "result": data
            }
        except json.JSONDecodeError:
            # 若JSON解析失败，返回原始内容
            return {
                "result": [["错误", "JSON解析失败"]]
            }
    else:
        print(f"{final_output}")


if __name__ == '__main__':
    asyncio.run(run_search())
