from openai import OpenAI

def start_LLM_model(type="4.0"):
    if type == "4.0":
        client = OpenAI(
            base_url="https://kap.chatgptapi.org.cn/v1",
            api_key="sk-A6b4r0dohTVc3898404d6e7b7869410d8e74D5C01e209e07"
        )
        model = "gpt-4"
    elif type == "3.5":
        client = OpenAI(
            base_url="https://api.chatgptid.net/v1",
            api_key="sk-qlSP8rekTxHK7x2fE7E3130319C94cD0B506Fc40C735AfC0"
        )
        model = "gpt-3.5-turbo"
    return client, model