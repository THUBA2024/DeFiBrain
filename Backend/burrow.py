import requests 
import ast
import json


def transform_element(original_element):
    burrow_element = {
        "name": "burrow_" + original_element["symbol"],
        "borrow_apy": original_element["borrow_apy"],
        "price": original_element["price"],
        "symbol": original_element["symbol"],
        "token": original_element["token"],
        "total_borrow_price": original_element["total_burrow_price"],
        "type": "borrow",
        "link": "https://app.burrow.finance/tokenDetail/"+original_element["token"]
    }
    
    supply_element = {
        "name": "burrow_" + original_element["symbol"],
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


def update_burrow():
    url = 'http://localhost:8100/list_token_data'
    response = requests.get(url) 
    converted_dict = ast.literal_eval(response.text)["data"]
    # print(converted_dict)

    new_list = []
    for item in converted_dict:
        temp1, temp2 = transform_element(item)
        new_list.append(temp1)
        new_list.append(temp2)

    # print(new_list)

    with open("storage/burrow.json", 'w') as json_file:
        json.dump(new_list, json_file, indent=4)