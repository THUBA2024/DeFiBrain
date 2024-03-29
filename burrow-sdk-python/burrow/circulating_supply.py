import requests
from datetime import datetime
from burrow.contract_handler import BurrowHandler
import burrow.globals as globals
from config import GlobalConfig


global_config = GlobalConfig()

signer = globals.get_signer_account(global_config.signer_account_id)

# token account
brrr_token = 'token.burrow.near'
# set all accounts with locked tokens
brrr_locked_holders = ['lockup.burrow.near', 'burrow.sputnik-dao.near']
# token max supply
max_supply = 10 ** 9


def get_token_price(token_id):
    try:
        response = requests.get("https://indexer.ref.finance/get-token-price?token_id=" + token_id)
        json_data = response.json()
        return float(json_data["price"])
    except Exception as e:
        print(f"Error fetching token price: {e}")
        return 0


def update_marketcap():
    market_cap = {
        "lockedBalances": [],
        "circulatingSupply": 0,
        "lastUpdate": 0
    }

    token_price = get_token_price("token.burrow.near")

    locked_balances = []
    for address in brrr_locked_holders:
        burrow_handler = BurrowHandler(signer, brrr_token)
        ft_balance = burrow_handler.ft_balance_of(address)
        parsed_balance = int(ft_balance) / (10 ** 18)
        value = parsed_balance * token_price
        locked_balances.append({
            "address": address,
            "balance": parsed_balance,
            "value": value
        })

    sum_locked = sum([balance["balance"] for balance in locked_balances])
    circulating_supply = max_supply - sum_locked
    if circulating_supply is not None:
        market_cap["lockedBalances"] = locked_balances
        market_cap["circulatingSupply"] = circulating_supply
        market_cap["lastUpdate"] = datetime.now().timestamp()
    return market_cap


def get_circulating_supply():
    token_price = get_token_price("token.burrow.near")

    locked_balances = []
    for address in brrr_locked_holders:
        burrow_handler = BurrowHandler(signer, brrr_token)
        ft_balance = burrow_handler.ft_balance_of(address)
        parsed_balance = int(ft_balance) / (10 ** 18)
        value = parsed_balance * token_price
        locked_balances.append({
            "address": address,
            "balance": parsed_balance,
            "value": value
        })
    sum_locked = sum([balance["balance"] for balance in locked_balances])
    circulating_supply = max_supply - sum_locked
    return circulating_supply


if __name__ == "__main__":
    print("############START###########")
    market_cap = update_marketcap()
    print(market_cap)
