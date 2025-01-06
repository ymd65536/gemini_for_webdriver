import os
import vertexai
from vertexai.preview.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    Tool
)

# Function Callingで呼び出すメソッド


def open_window(url, action) -> str:
    if action == "Microsoft Edge":
        url = f"microsoft-edge:{url}"
    elif action == "Google Chrome":
        url = f"googlechrome:{url}"
    elif action == "Firefox":
        url = f"firefox:{url}"
    else:
        url = f"{url}"
    return url


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
            "action": {
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
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0},
        tools=[webdriver_tool],
    )
    return response


if __name__ == "__main__":

    # prompt = "https://www.google.com/ をMicrosoft Edgeのウィンドウで開く"
    prompt = "https://www.google.com/ をSafariのウィンドウで開く"
    response = function_calling(prompt)
    print("------")
    if response.candidates[0].content.parts[0].function_call.name:
        print(
            f"最適な関数 : {response.candidates[0].content.parts[0].function_call.name}")
        print(
            f"必要な引数 : {response.candidates[0].content.parts[0].function_call.args.get('url')}")
        print(
            f"必要な引数 : {response.candidates[0].content.parts[0].function_call.args.get('action')}")
    else:
        print("最適な関数 : 何もなし")

    response = function_calling(prompt)

    if response.candidates[0].content.parts[0].function_call:
        # 関数名を取得
        function_name = response.candidates[0].content.parts[0].function_call.name
        url = response.candidates[0].content.parts[0].function_call.args.get(
            "url")

        action = response.candidates[0].content.parts[0].function_call.args.get(
            "action")

        # 実行可能な関数
        available_functions = {
            "open_window": open_window
        }
        exec_function = available_functions[function_name]

        # 関数を実行
        function_response = exec_function(url, action)
        print(f"{function_response}")
    else:
        print("最適な関数 : 何もなし")
