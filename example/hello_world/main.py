import requests
import config.const as const
import os
import vertexai
from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Tool
)

# Function Callingで呼び出すメソッド


def open_window(url, browser) -> str:
    if browser == "Microsoft Edge":
        url = f"microsoft-edge:{url}"
    elif browser == "Google Chrome":
        res = requests.post(
            const.WEB_DRIVER_URL,
            headers={'Content-Type': 'application/json'},
            data='{"capabilities":{}}'
        ).json()

        # セッションIDを取得
        sessionId = res.get("value").get("sessionId")
        res = requests.post(
            "".join([const.WEB_DRIVER_URL, '/', sessionId, '/url']),
            headers={'Content-Type': 'application/json'},
            data='{"url": "' + url + '"}'
        ).json()
        return sessionId
    elif browser == "Firefox":
        url = f"firefox:{url}"
    else:
        url = f"{url}"
    return None


PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = "us-central1"

# Vertex AI インスタンスの初期化
vertexai.init(project=PROJECT_ID, location=LOCATION)

# モデルの初期化
model = GenerativeModel("gemini-pro")

# 関数を定義
open_window_func = FunctionDeclaration(
    name="open_window",
    description="指定されたURLを指定されたブラウザのウィンドウで開く",
    parameters={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL"
            },
            "browser": {
                "type": "string",
                "description": "ブラウザで開く"
            }
        }
    },
)

# LLM が呼び出すツールを定義
webdriver_tool = Tool(
    function_declarations=[open_window_func],
)

# Function calling 関数を定義


def function_calling(prompt) -> dict:
    if const.WEB_DRIVER_URL is None:
        raise ValueError("WEBDRIVER_PORT is not set")
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0},
        tools=[webdriver_tool],
    )
    return response


if __name__ == "__main__":

    prompt = "https://www.google.com/ をGoogle Chromeのウィンドウで開く"
    response = function_calling(prompt)

    if response.candidates[0].content.parts[0].function_call:
        # 関数名を取得
        function_name = response.candidates[0].content.parts[0].function_call.name
        url = response.candidates[0].content.parts[0].function_call.args.get(
            "url")

        browser = response.candidates[0].content.parts[0].function_call.args.get(
            "browser")

        # 実行可能な関数
        available_functions = {
            "open_window": open_window
        }
        exec_function = available_functions[function_name]

        # 関数を実行
        function_response = exec_function(url, browser)
        if function_response is not None:
            print("実行結果 : ", function_response)

    else:
        print("最適なアクションなし")
