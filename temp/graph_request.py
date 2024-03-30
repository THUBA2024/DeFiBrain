import requests


def Grequest(query):
    key = "2fd57c65d0e051dea3ac417bdf3f6ad2"
    url = "https://gateway-arbitrum.network.thegraph.com/api/2fd57c65d0e051dea3ac417bdf3f6ad2/subgraphs/id/QmdAmQxQCuGoeqNLuE8m6zH366pY2LkustTRYDhSt85X7w"
    response = requests.post(url, json={'query': query})
    data = response.json()
    return data


# temp = "https://api.thegraph.com/subgraphs/name/aave/protocol-v3/graphql?query="

query = """
{
  reserves {
    id
    name
    underlyingAsset
    
    liquidityRate 
    stableBorrowRate
    variableBorrowRate
  }
}
    """

# url = "https://api.thegraph.com/subgraphs/name/aave/protocol-v3/graphql?query=%7B%0A++reserves+%7B%0A++++name%0A++++underlyingAsset%0A++++%0A++++liquidityRate+%0A++++stableBorrowRate%0A++++variableBorrowRate%0A++%7D%0A%7D"

# response = requests.post(url)
# data = response.json()

data = Grequest(query)
print(data)