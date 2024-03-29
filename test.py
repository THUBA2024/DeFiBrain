import requests
import json

# 测试用的 URL，根据你的 Flask 应用运行的地址可能需要修改
url = 'http://127.0.0.1:5000/request'

# 准备测试数据，这里是 JSON 格式的数据
data = {
    'query': '我想借usdc'
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 打印响应内容
print('Status Code:', response.status_code)
print('Response:', response.json())