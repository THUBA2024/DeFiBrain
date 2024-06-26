import requests
from tools.token_price import get_crypto_prices
import json
from datetime import datetime, timedelta
import time

RAY = 10**27
SECONDS_PER_YEAR = 31536000

def timestamp_x_days_ago(x):
    now = datetime.now()
    x_days_ago = now - timedelta(days=x)
    timestamp = int(time.mktime(x_days_ago.timetuple()))
    return timestamp


def calc_APY(unray):
  apr = unray / RAY
  apy = ((1 + (apr / SECONDS_PER_YEAR)) ** SECONDS_PER_YEAR) - 1
  apy = apy * 100
  return apy

def get_graph_data(query, link='https://api.thegraph.com/subgraphs/name/aave/protocol-v3'):
  subgraph_endpoint = link

  response = requests.post(subgraph_endpoint, json={'query': query})

  # print(response.json())
  data = response.json()["data"]

  print(data)
  return data

def data_prepare(data):
  new_data = []
  for item in data:
    if item["symbol"] == "PYUSD" or item["symbol"] == "USDC" or item["symbol"] == "USDT":
      item["totalCurrentVariableDebt"]+="000000000000"
      item["totalSupplies"]+="000000000000"
    elif item["symbol"] == "WBTC":
      item["totalCurrentVariableDebt"]+="0000000000"
      item["totalSupplies"]+="0000000000"
    price = get_crypto_prices(item["symbol"])
    borrow_element = {
        "name":  "AAVE_"+item["name"],
        "token": item["underlyingAsset"],
        "symbol": item["symbol"],
        "borrow_apy": format(calc_APY(int(item["variableBorrowRate"])), '.2f'),
        "total_borrow_price": str(round(float(item["totalCurrentVariableDebt"])/10**18 * price, 6)),
        "type": "borrow",
        "price": round(price, 4),
        "link": "https://app.aave.com/reserve-overview/?underlyingAsset="+item["underlyingAsset"]+"&marketName=proto_mainnet_v3"
    }
    supply_element = {
        "name": "AAVE_"+item["name"],
        "token": item["underlyingAsset"],
        "symbol": item["symbol"],
        "supply_apy": format(calc_APY(int(item["liquidityRate"])), '.2f'),
        "total_supplied_price": str(round(float(item["totalSupplies"])/10**18 * price, 6)),
        "type": "supply",
        "price": round(price, 4),
        "link": "https://app.aave.com/reserve-overview/?underlyingAsset="+item["underlyingAsset"]+"&marketName=proto_mainnet_v3"
    }
    new_data.append(borrow_element)
    new_data.append(supply_element)
  return new_data

# print(calc_APY(116859139781528081735574962))

# Define the GraphQL query
# liquidityRate means supply rate

# data = get_graph_data(query)
# data_list = data_prepare(data)


# with open("aave.json", 'w') as json_file:
#     json.dump(data_list, json_file, indent=4)


def update_aavm():
  query = """
  {
    reserves {
      id
      name
      symbol
      underlyingAsset
      
      liquidityRate 
      stableBorrowRate
      variableBorrowRate

      totalSupplies
      totalCurrentVariableDebt
      
    }
  }
      """
  data = get_graph_data(query)["reserves"]
  data_list = data_prepare(data)


  with open("storage/aave.json", 'w') as json_file:
      json.dump(data_list, json_file, indent=4)


def query_symbol(symbol):
  time_stap = timestamp_x_days_ago(30)
  query = """
    {{
      borrows(
        orderBy: timestamp
        orderDirection: desc
        where: {{reserve_: {{symbol: "{symbol}"}}, timestamp_gte: {time_stap}}}
      ) {{
        timestamp
        assetPriceUSD
        amount
        borrowRate
        variableTokenDebt
      }}
    }}
    """.format(symbol=symbol,time_stap=time_stap)
  data = get_graph_data(query)
  # print(data)
  return data

def query_testtrain_borrows():
  time_stap = timestamp_x_days_ago(30)
  query = """
    query MyQuery {{
      borrows(
        orderBy: blockTimestamp
        orderDirection: desc
        where: {{blockTimestamp_gt: {time_stap}}}
      ) {{
        amount
        borrowRate
        user
        reserve
        interestRateMode
        blockTimestamp
      }}
    }}
  """.format(time_stap=time_stap)

  data = get_graph_data(query,link="https://gateway-arbitrum.network.thegraph.com/api/2fd57c65d0e051dea3ac417bdf3f6ad2/subgraphs/id/CvTeB7ja6sz9MdmHd2GjVPRgEDh6U5MFTZ5jkGA5Hcf9")
  print(data)
  return data


def query_testtrain_supplys():
  time_stap = timestamp_x_days_ago(30)
  query = """
    query MyQuery {{
      supplies(
        orderBy: blockTimestamp
        orderDirection: desc
        where: {{blockTimestamp_gt: {time_stap}}}
      ) {{
        blockTimestamp
        reserve
        user
        amount
      }}
    }}
  """.format(time_stap=time_stap)

  data = get_graph_data(query,link="https://gateway-arbitrum.network.thegraph.com/api/2fd57c65d0e051dea3ac417bdf3f6ad2/subgraphs/id/CvTeB7ja6sz9MdmHd2GjVPRgEDh6U5MFTZ5jkGA5Hcf9")
  print(data)
  return data


# print(timestamp_x_days_ago(30))
# query_testtrain_supplys()





# from graphql_request import GraphQLClient 
# client = GraphQLClient("https://api.thegraph.com/subgraphs/name/aave/protocol-v3")

# query = """
# {
#   reserves {
#     name
#     underlyingAsset
    
#     liquidityRate 
#     stableBorrowRate
#     variableBorrowRate
#   }
# }
#     """


# result = client.execute(query)
# print(result)