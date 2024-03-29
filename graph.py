import requests

RAY = 10**27
SECONDS_PER_YEAR = 31536000

def calc_APY(unray):
  apr = unray / RAY
  apy = ((1 + (apr / SECONDS_PER_YEAR)) ** SECONDS_PER_YEAR) - 1
  apy = apy * 100
  return apy

def get_graph_data(query):
  subgraph_endpoint = 'https://api.thegraph.com/subgraphs/name/aave/protocol-v3'

  response = requests.post(subgraph_endpoint, json={'query': query})

  data = response.json()["data"]["reserves"]

  print(data)
  return data

def data_prepare(data):
  new_data = []
  for item in data:
    borrow_element = {
        "name": item["name"],
        "token": item["underlyingAsset"],
        "symbol": item["symbol"],
        "borrow_apy": calc_APY(int(item["variableBorrowRate"])),
        "total_borrow_price": original_element["total_burrow_price"],
        "type": "borrow",
        "link": "https://app.burrow.finance/tokenDetail/"+original_element["token"]
    }

# print(calc_APY(116859139781528081735574962))

# Define the GraphQL query
# liquidityRate means supply rate
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
    
  }
}
    """

# # Define the subgraph's endpoint
# subgraph_endpoint = 'https://api.thegraph.com/subgraphs/name/aave/protocol-v3'

# # Make the GraphQL query
# response = requests.post(subgraph_endpoint, json={'query': query})

# # Print the response
# data = response.json()
# print(response.json())


get_graph_data(query)













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