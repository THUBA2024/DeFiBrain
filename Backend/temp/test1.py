import json

with open('burrow.json', 'r') as file:
    json_data = json.load(file)

extracted_data = []
for item in json_data:
    extracted_item = {
        "symbol": item["symbol"],
        "type": item["type"]
    }
    
    if item["type"] == "burrow":
        extracted_item["apy"] = item.get("borrow_apy")
        extracted_item["total_price"] = item.get("total_burrow_price")
    elif item["type"] == "supply":
        extracted_item["apy"] = item.get("supply_apy")
        extracted_item["total_price"] = item.get("total_supplied_price")
    
    extracted_data.append(extracted_item)


extracted_json_text = json.dumps(extracted_data, indent=4)
print(extracted_json_text)