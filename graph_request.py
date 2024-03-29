import requests



query = """
{
  interestRates(first: 10, where: {side: LENDER}) {
    duration
    id
    maturityBlock
    rate
    side
    tranche
    type
  }
}
    """

key = "2fd57c65d0e051dea3ac417bdf3f6ad2"
url = "https://gateway-arbitrum.network.thegraph.com/api/2fd57c65d0e051dea3ac417bdf3f6ad2/subgraphs/id/JCNWRypm7FYwV8fx5HhzZPSFaMxgkPuw4TnR3Gpi81zk"
response = requests.post(url, json={'query': query})
data = response.json()
print(data)