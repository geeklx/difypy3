import asyncio
import os
import shutil

from dotenv import load_dotenv
import httpx

load_dotenv()

# Settings
# DIFY_ORIGIN = os.getenv("DIFY_ORIGIN", "http://localhost")  # Dify origin URL
# EMAIL = os.getenv("EMAIL")  # Login email
# PASSWORD = os.getenv("PASSWORD")  # Login password
DIFY_ORIGIN = "http://localhost"
EMAIL = "liangxiao6@live.com"
PASSWORD = "wuyusheng@2011"

BASE_URL = f"{DIFY_ORIGIN}/console/api"  # Base URL for API
DSL_FOLDER_PATH = "./dsl"  # Folder to save YML files


client = httpx.AsyncClient()  # Global AsyncClient instance
# Set a maximum of 3 concurrent tasks
MAX_CONCURRENT_TASKS = 3
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)


async def execute_api(
    url: str,
    access_token: str | None = None,
    params: dict[str, str] | None = None,
    payload: dict[str, str] | None = None,
    method_type: str = "GET",
    retries: int = 3,
) -> dict:
    """
    Execute an API request.
    """
    headers = {"Authorization": f"Bearer {access_token}"} if access_token else None
    async with semaphore:
        for attempt in range(retries):
            match method_type:
                case "POST":
                    response = await client.post(
                        url, headers=headers, params=params, json=payload
                    )
                case "GET":
                    response = await client.get(url, headers=headers, params=params)
                case _:
                    raise ValueError("Invalid method type")

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Attempt {attempt + 1} failed: {response.status_code} - {url}")
                await asyncio.sleep(0.5)  # Wait before retrying

    raise Exception(f"Failed to request api: {url}")


async def login_and_get_token() -> str:
    """
    Log in and get the access token.

    :return: The obtained access token
    :raises Exception: If login fails
    """
    payload = {"email": EMAIL, "password": PASSWORD}
    url = f"{BASE_URL}/login"
    response = await execute_api(url, payload=payload, method_type="POST")
    if response.get("result") == "success":
        access_token = response["data"]["access_token"]
        print("Access token obtained successfully")
        return access_token
    else:
        print(f"Login API error: {response.get("result")} - {url}")
    raise Exception("Login failed")


async def fetch_app_per_page(
    access_token: str, page: int, limit: int, retries: int = 3
) -> dict:
    """
    Fetch the list of apps per page.

    :param access_token: The access token
    :param page: The page number to fetch
    :param limit: The number of items per page
    :param retries: The number of retry attempts (default: 3)
    :return: The app data
    :raises Exception: If fetching app data fails
    """
    return await execute_api(
        f"{BASE_URL}/apps",
        access_token=access_token,
        params={"page": page, "limit": limit},
        method_type="GET",
    )


async def get_app_list(access_token: str) -> tuple[list, int]:
    """
    Get a list of all apps and the total number of apps.

    :param access_token: The access token
    :return: A tuple containing a list of app information and the total number of apps
    """
    app_list = []
    page = 1
    limit = 30
    app_num = 0
    while True:
        content = await fetch_app_per_page(access_token, page, limit)

        if page == 1:
            # Calculate total pages from the first API response
            app_num = content.get("total", 0)
            max_page_num = app_num // limit + (app_num % limit > 0)
            print(f"Total apps: {app_num}, Total pages: {max_page_num}")

        if app_num == 0:
            return [], 0

        if page > max_page_num:
            break

        app_per_page = [
            {"id": app.get("id"), "name": app.get("name")}
            for app in content.get("data", [])
        ]
        app_list.extend(app_per_page)
        page += 1

    return app_list, app_num


def create_dsl_folder():
    """
    Create a folder to save the YML files.

    If the folder already exists, it will be deleted and recreated.
    """
    if os.path.exists(DSL_FOLDER_PATH):
        shutil.rmtree(DSL_FOLDER_PATH)
    os.makedirs(DSL_FOLDER_PATH)


async def download_yml_files(access_token: str, apps: list):
    """
    Download YML files for each app concurrently.

    :param access_token: The access token
    :param apps: A list of apps (with ID and name)
    """
    create_dsl_folder()  # Create folder to save YML files
    tasks = [asyncio.create_task(download_yml_file(access_token, app)) for app in apps]
    await asyncio.gather(*tasks)  # Run all download tasks concurrently


async def download_yml_file(access_token, app, retries=3):
    """
    Download the YML file for a single app.

    :param access_token: The access token
    :param app: The app's information (ID and name)
    :param retries: The number of retry attempts (default: 3)
    """
    url = f"{BASE_URL}/apps/{app["id"]}/export?include_secret=true"
    # Limit the maximum number of concurrent tasks using a semaphore
    response = await execute_api(url, access_token, method_type="GET")
    dsl_data = response.get("data").encode("utf-8")
    replace_app_name = replace_appname(app["name"])
    file_name = f"{DSL_FOLDER_PATH}/{replace_app_name}.yml"

    with open(file_name, "wb") as file:
        file.write(dsl_data)
    print(f"Downloaded: {file_name}")


def replace_appname(app_name):
    """
    Replace the app name.

    :param app_name: The original app name
    :return: The modified app name
    """
    return app_name.replace("/", "-")


async def main():
    """
    Main processing: Obtain access token, get app list, and download YML files.

    First, obtain the access token and app list, then download YML files for each app.
    """
    # 1. Get access token
    access_token = await login_and_get_token()
    if not access_token:
        print("Failed to obtain access token.")
        return

    # 2. Get the list of apps
    app, app_num = await get_app_list(access_token)
    print(f"Fetched app list: {app}")

    # 3. Check download feasibility
    if not app:
        print("No apps found.")
        return
    if len(app) != app_num:
        print("Mismatch in the number of apps.")
        return

    # 4. Download YML files for all apps concurrently
    await download_yml_files(access_token, app)

    # 5. Close the client after finishing
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
