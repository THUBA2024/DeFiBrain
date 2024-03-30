def filter_symbol(json_data):
    for i in range(len(json_data)):
        if json_data[i]["name"].split("_")[0] == "burrow" and json_data[i]["symbol"] == "USDt":
            json_data[i]["symbol"] = "USDT"
        elif json_data[i]["name"].split("_")[0] == "AAVE" and json_data[i]["symbol"] == "WETH":
            json_data[i]["symbol"] = "ETH"
    return json_data