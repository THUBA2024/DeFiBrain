import requests
from time import sleep

def get_crypto_prices(symbol):
    symbol = symbol.upper()
    if symbol=="CBETH":
        symbol="cbETH"
    
    api_key = 'dcbf10f7-68dd-43c1-840a-ec5d5fbac3f8'
    
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    try_time = 0
    while try_time<=2:
        response = requests.get(url, headers=headers)
        data = response.json()
        # print(data['data'])
        if 'data' in data:
            price = data['data'][symbol]['quote']['USD']['price']
            print(price)
        else:
            print("Try again.")
            sleep(2)
            try_time+=1
            continue
        return price
    print("Error fetching data. Check your API key and try again.")

if __name__ == "__main__":
    get_crypto_prices("SDAI")