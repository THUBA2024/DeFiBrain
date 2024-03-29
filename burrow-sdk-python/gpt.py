from openai import OpenAI
import re

# client = OpenAI(
#     base_url="https://api.chatgptid.net/v1",
#     api_key="sk-qlSP8rekTxHK7x2fE7E3130319C94cD0B506Fc40C735AfC0"
# )

client = OpenAI(
    base_url="https://api.openai.com/v1/chat/completions",
    api_key="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"
)


completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "user", "content": 
     '''
    接下来我会提供一些产品的信息，会以json格式提供，另外用户会提出一些需求（例如找到收益率最高的产品），你需要在所提供的信息中选取最合适的一到两个，返回其产品符号，并给出100字左右简要介绍为什么选择这个产品，回答格式如下：{symbol:<符号>,note:<回答的文本>}请注意回答不要包含其他内容，提供的信息如下：

产品信息（其中"available_liquidity_price"代表池子总金额，"total_burrow_price"代表借贷总金额，"total_supplied_balance"代表存款总金额，这三个均可用于判断稳定性；"borrow_apy"代表借贷年利率；"supply_apy"代表存款年利率；"symbol"代表产品符号，用于返回）：

{"available_liquidity_price":"1999385.064248","borrow_apy":"0.00","price":0.011077143426,"supply_apy":"0.00","symbol":"BRRR","token":"token.burrow.near","total_burrow_balance":"0.000000","total_burrow_price":"0.000000","total_supplied_balance":"180677127.101292","total_supplied_price":"2001386.450699"},

{"available_liquidity_price":"381506.943465","borrow_apy":"2.38","price":3542.34,"supply_apy":"0.73","symbol":"ETH","token":"aurora","total_burrow_balance":"67.600473","total_burrow_price":"239463.859527","total_supplied_balance":"175.407412","total_supplied_price":"621352.691824"},

{"available_liquidity_price":"424566.581101","borrow_apy":"4.95","price":1.0001,"supply_apy":"3.25","symbol":"DAI","token":"6b175474e89094c44da98b954eedeac495271d0f.factory.bridge.near","total_burrow_balance":"836620.759397","total_burrow_price":"836704.421473","total_supplied_balance":"1261569.837163","total_supplied_price":"1261695.994147"},

{"available_liquidity_price":"282719.565318","borrow_apy":"14.60","price":1.0017,"supply_apy":"12.72","symbol":"USDT.e","token":"dac17f958d2ee523a2206206994597c13d831ec7.factory.bridge.near","total_burrow_balance":"1539701.901263","total_burrow_price":"1542319.394495","total_supplied_balance":"1822224.181273","total_supplied_price":"1825321.962381"},

{"available_liquidity_price":"246946.823433","borrow_apy":"15.78","price":0.9996,"supply_apy":"14.37","symbol":"USDC.e","token":"a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near","total_burrow_balance":"1410569.474288","total_burrow_price":"1410005.246498","total_supplied_balance":"1657862.408912","total_supplied_price":"1657199.263948"},

{"available_liquidity_price":"6133741.641244","borrow_apy":"4.68","price":7.453,"supply_apy":"1.14","symbol":"wNEAR","token":"wrap.near","total_burrow_balance":"393023.009401","total_burrow_price":"2929200.489066","total_supplied_balance":"1216836.443289","total_supplied_price":"9069082.011833"},

{"available_liquidity_price":"53794011.900517","borrow_apy":"0.03","price":9.5238,"supply_apy":"0.00","symbol":"STNEAR","token":"meta-pool.near","total_burrow_balance":"13141.060112","total_burrow_price":"125152.828295","total_supplied_balance":"5667171.988972","total_supplied_price":"53973012.588572"},

{"available_liquidity_price":"719262.216449","borrow_apy":"1.93","price":69151.9,"supply_apy":"0.47","symbol":"WBTC","token":"2260fac5e5542a773aa44fbcfedf7c193bc2c599.factory.bridge.near","total_burrow_balance":"4.746506","total_burrow_price":"328229.908261","total_supplied_balance":"15.158110","total_supplied_price":"1048212.106909"},

{"available_liquidity_price":"69886.405667","borrow_apy":"0.00","price":0.022152763941,"supply_apy":"0.00","symbol":"META","token":"meta-token.near","total_burrow_balance":"0.000000","total_burrow_price":"0.000000","total_supplied_balance":"3157906.716079","total_supplied_price":"69956.362029"},

{"available_liquidity_price":"106361.700388","borrow_apy":"2.62","price":0.4299,"supply_apy":"0.13","symbol":"AURORA","token":"aaaaaa20d9e0e2461697782ef11675f668207961.factory.bridge.near","total_burrow_balance":"16233.387683","total_burrow_price":"6978.733365","total_supplied_balance":"263891.374556","total_supplied_price":"113446.901922"},

{"available_liquidity_price":"123980199.701437","borrow_apy":"0.00","price":8.9491,"supply_apy":"0.00","symbol":"LINEAR","token":"linear-protocol.near","total_burrow_balance":"2376.019600","total_burrow_price":"21263.237002","total_supplied_balance":"13870173.228866","total_supplied_price":"124125567.242445"},

{"available_liquidity_price":"3708.662124","borrow_apy":"15.31","price":0.47109,"supply_apy":"7.79","symbol":"WOO","token":"4691937a7508860f876c9c0a2a617e7d9e945d4b.factory.bridge.near","total_burrow_balance":"13142.379453","total_burrow_price":"6191.243537","total_supplied_balance":"21022.772793","total_supplied_price":"9903.618035"},

{"available_liquidity_price":"5304.434608","borrow_apy":"0.00","price":8.738,"supply_apy":"0.00","symbol":"NearX","token":"v2-nearx.stader-labs.near","total_burrow_balance":"2.226580","total_burrow_price":"19.455856","total_supplied_balance":"609.887870","total_supplied_price":"5329.200208"},

{"available_liquidity_price":"4113914.418254","borrow_apy":"4.80","price":1.0017,"supply_apy":"2.38","symbol":"USDt","token":"usdt.tether-token.near","total_burrow_balance":"7433042.554122","total_burrow_price":"7445678.726464","total_supplied_balance":"11544086.230577","total_supplied_price":"11563711.177169"},

{"available_liquidity_price":"3303464.134542","borrow_apy":"5.00","price":0.9996,"supply_apy":"2.59","symbol":"USDC","token":"17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1","total_burrow_balance":"6722504.808790","total_burrow_price":"6719815.806866","total_supplied_balance":"10030598.951895","total_supplied_price":"10026586.712314"},

{"available_liquidity_price":"548610.073122","borrow_apy":"0.00","price":0.9975,"supply_apy":"0.00","symbol":"FRAX","token":"853d955acef822db058eb8505911ed77f175b99e.factory.bridge.near","total_burrow_balance":"0.000000","total_burrow_price":"0.000000","total_supplied_balance":"550535.571283","total_supplied_price":"549159.232355"},

{"available_liquidity_price":"5.098396","borrow_apy":"0.00","price":1.0207,"supply_apy":"0.00","symbol":"sFRAX","token":"a663b02cf0a4b149d2ad41910cb81e23e1c41c32.factory.bridge.near","total_burrow_balance":"0.000000","total_burrow_price":"0.000000","total_supplied_balance":"5.000000","total_supplied_price":"5.103500"}]}

用户提问：我想要借钱，哪个最划算
    '''
     
     }
  ]
)

note = re.search(r'note:\s*"([^"]+)"', completion.choices[0].message.content).group(1) if completion.choices else None
print(completion)