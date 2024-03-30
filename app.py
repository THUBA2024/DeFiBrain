from flask import Flask, request, jsonify
from openai import OpenAI
import re
import ast
import json
from flask_cors import CORS
from graph import update_aavm
from burrow import update_burrow
from tools.filter import filter_symbol

app = Flask(__name__)
CORS(app)

def read_prompt_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    return prompt

def get_burrow_data(path="storage/burrow.json"):
    with open(path, 'r') as file:
        json_data = json.load(file)

    json_data = filter_symbol(json_data)
    # print(json_data)

    extracted_data = []
    data_dict = {}
    for item in json_data:

        data_dict[(item["symbol"],item["type"],item["name"].split("_")[0])] = item

        extracted_item = {
            "protocol": item["name"].split("_")[0],
            "symbol": item["symbol"],
            "type": item["type"]
        }
        
        if item["type"] == "borrow":
            extracted_item["apy"] = item.get("borrow_apy")
            extracted_item["total_price"] = item.get("total_borrow_price")
        elif item["type"] == "supply":
            extracted_item["apy"] = item.get("supply_apy")
            extracted_item["total_price"] = item.get("total_supplied_price")
        
        extracted_data.append(extracted_item)
    extracted_json_text = json.dumps(extracted_data, indent=4)
    return extracted_json_text, data_dict
    # print(extracted_json_text)

def get_aave_data(path="storage/aave.json"):
    with open(path, 'r') as file:
        json_data = json.load(file)

    json_data = filter_symbol(json_data)

    extracted_data = []
    data_dict = {}
    for item in json_data:

        data_dict[(item["symbol"],item["type"],item["name"].split("_")[0])] = item

        extracted_item = {
            "protocol": item["name"].split("_")[0],
            "symbol": item["symbol"],
            "type": item["type"]
        }
        
        if item["type"] == "borrow":
            extracted_item["apy"] = item.get("borrow_apy")
            extracted_item["total_price"] = item.get("total_borrow_price")
        elif item["type"] == "supply":
            extracted_item["apy"] = item.get("supply_apy")
            extracted_item["total_price"] = item.get("total_supplied_price")
        
        extracted_data.append(extracted_item)
    extracted_json_text = json.dumps(extracted_data, indent=4)
    return extracted_json_text, data_dict
    # print(extracted_json_text)


@app.route('/request', methods=['POST'])
def get_best_product():
    data_burrow, data_dict_burrow = get_burrow_data()
    data_aave, data_dict_aave = get_aave_data()

    # merge
    data_dict_burrow.update(data_dict_aave)
    data_dict = data_dict_burrow


    ask_data = request.json  
    prompt = read_prompt_from_file('prompt-en.txt')
    user_query = prompt + data_burrow.replace("]",",") + data_aave + "\n User questions:" + ask_data.get('query')  # 从 JSON 中提取用户的查询内容
    print(user_query)

    client = OpenAI(
        base_url="https://api.chatgptid.net/v1",
        api_key="sk-qlSP8rekTxHK7x2fE7E3130319C94cD0B506Fc40C735AfC0"
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    # print(completion.choices[0].message.content)
    # 解析回复，获取 note
    note = completion.choices[0].message.content if completion.choices else None
    return_dict = ast.literal_eval(note)
    # print(data_dict)
    selected_data = data_dict[(return_dict["symbol"],return_dict["type"],return_dict["protocol"])]
    print(return_dict)

    print(data_dict[(return_dict["symbol"],return_dict["type"],return_dict["protocol"])])

    return jsonify({"symbol": return_dict["symbol"],
                    "reply": return_dict["reply"],
                    "type": return_dict["type"],
                    "protocol": return_dict["protocol"],
                    "link": selected_data["link"] if "link" in selected_data else None,
                    "price": selected_data["price"],
                    "apy": selected_data[return_dict["type"]+"_apy"]})


if __name__ == '__main__':
    # update_aavm()
    # update_burrow()
    app.run(host='0.0.0.0', port=5000, debug=False)