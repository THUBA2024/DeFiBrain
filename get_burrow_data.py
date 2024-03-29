import requests 
import ast
import json


url = 'http://localhost:8100/list_token_data'


response = requests.get(url) 
# response = requests.post(url, json=data) 
converted_dict = ast.literal_eval(response.text)["data"]
# print(converted_dict) # 打印出响应的内容


def transform_element(original_element):
    # 创建第一个元素
    burrow_element = {
        "borrow_apy": original_element["borrow_apy"],
        "price": original_element["price"],
        "symbol": original_element["symbol"],
        "token": original_element["token"],
        "total_borrow_price": original_element["total_burrow_price"],
        "type": "borrow",
        "link": "https://app.burrow.finance/tokenDetail/"+original_element["token"]
    }
    
    # 创建第二个元素
    supply_element = {
        "supply_apy": original_element["supply_apy"],
        "price": original_element["price"],
        "symbol": original_element["symbol"],
        "token": original_element["token"],
        "total_supplied_price": original_element["total_supplied_price"],
        "type": "supply",
        "link": "https://app.burrow.finance/tokenDetail/"+original_element["token"]
    }
    
    # 返回包含两个新元素的列表
    return burrow_element, supply_element

new_list = []
for item in converted_dict:
    temp1, temp2 = transform_element(item)
    new_list.append(temp1)
    new_list.append(temp2)

# print(new_list)

with open("burrow.json", 'w') as json_file:
    json.dump(new_list, json_file, indent=4)