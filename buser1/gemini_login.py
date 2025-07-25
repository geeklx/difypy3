import asyncio
import json

from playwright.async_api import async_playwright


async def save_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.taobao.com")

        print("请手动登录淘宝，登录成功后按回车继续...")
        input("回车键继续...")  # 等你手动登录好

        # 获取所有 cookies
        cookies = await context.cookies()
        with open("taobao_cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)

        print("✅ Cookies 已保存到 taobao_cookies.json")
        await browser.close()


if __name__ == '__main__':
    asyncio.run(save_cookies())
