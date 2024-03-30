import requests
import json
from burrow.contract_handler import BurrowHandler
import burrow.globals as globals

from config import GlobalConfig
from burrow.tool_util import success, error

global_config = GlobalConfig()
signer = globals.get_signer_account(global_config.signer_account_id)


def get_account_near_balance(account_id):
    data = {
        "jsonrpc": "2.0",
        "id": "dontcare",
        "method": "query",
        "params": {
            "request_type": "view_account",
            "finality": "final",
            "account_id": account_id
        }
    }
    headers = {"Content-type": "application/json"}
    response = requests.post(global_config.rpc_url, data=json.dumps(data), headers=headers).json()
    amount = int(response["result"]["amount"])
    storage_usage = int(response["result"]["storage_usage"])
    balance = (amount - storage_usage * multiply_decimals(19)) / multiply_decimals(24)
    return balance


def send_message(message):
    url = "http://127.0.0.1:8400/api/message/send"
    requests.packages.urllib3.disable_warnings()
    json_p = {
        "content": json.dumps(message),
        "product": "oracle",
        "level": "medium",
        "email": True,
        "telegram": True,
        "slack": True,
        "type": "alert"
    }
    ret_message = requests.post(url=url, verify=False, json=json_p).content
    ret_message = json.loads(ret_message)
    return ret_message


def multiply_decimals(decimals: int):
    return int("1" + "0" * decimals)


def handler_decimal(number, index):
    return ("{:.%sf}" % index).format(number)


def storage_balance_of(account_id, token_id):
    burrow_handler = BurrowHandler(signer, token_id)
    ret = burrow_handler.storage_balance_of(account_id)
    return success(ret)


def storage_deposit(account_id, token_id, amount):
    burrow_handler = BurrowHandler(signer, token_id)
    ret = burrow_handler.storage_deposit(account_id, int(amount))
    return success(ret)


def get_assets_paged_detailed():
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_assets_paged_detailed()
    return success(ret)


def get_asset_farms_paged():
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_asset_farms_paged()
    return success(ret)


def get_account(account_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_account(account_id)
    return success(ret)


def get_price_data():
    burrow_handler = BurrowHandler(signer, global_config.priceoracle_contract)
    ret = burrow_handler.get_price_data()
    return success(ret)


def ft_metadata(account_id):
    burrow_handler = BurrowHandler(signer, account_id)
    ret = burrow_handler.ft_metadata()
    return success(ret)


def get_token_price(token_id):
    try:
        response = requests.get("https://indexer.ref.finance/get-token-price?token_id=" + token_id)
        json_data = response.json()
        return float(json_data["price"])
    except Exception as e:
        print(f"Error fetching token price: {e}")
        return 0


def get_price():
    url = "https://raw.githubusercontent.com/NearDeFi/token-prices/main/ref-prices.json"
    requests.packages.urllib3.disable_warnings()
    ret = requests.get(url=url, verify=False)
    price_data = json.loads(ret.text)
    return price_data


def handle_token_price(price_data_list):
    token_price_data = {}
    price_list = get_price()
    for price_data in price_data_list["prices"]:
        price = price_data["price"]
        if price is None:
            continue
        token_metadata = ft_metadata(price_data["asset_id"])["data"]
        p = int(price["multiplier"]) / multiply_decimals((price["decimals"] - token_metadata["decimals"]))
        token_price_data[price_data["asset_id"]] = {"price": p, "symbol": token_metadata["symbol"],
                                                    "decimals": token_metadata["decimals"]}
    for key, value in price_list.items():
        token_price_data[key] = {"price": float(value["price"]), "symbol": value["symbol"], "decimals": value["decimal"]}
    return token_price_data


def handle_extra_decimals():
    assets_data_list = get_assets_paged_detailed()["data"]
    extra_decimals = {}
    for assets_data in assets_data_list:
        extra_decimals[assets_data["token_id"]] = assets_data["config"]["extra_decimals"]
    return extra_decimals


def handle_supply_farm_apy(assets_data, token_price_data, extra_decimals):
    supply_farm_apy = "0.00"
    supplied = assets_data["supplied"]["balance"]
    farms = assets_data["farms"]
    token_id = assets_data["token_id"]
    for farm in farms:
        if "Supplied" in farm["farm_id"]:
            for k, v in farm["rewards"].items():
                decimals = token_price_data[k]["decimals"] + extra_decimals[k]
                r = (int(v["reward_per_day"]) / multiply_decimals(decimals)) * float(token_price_data[k]["price"])
                s_decimals = token_price_data[token_id]["decimals"] + extra_decimals[token_id]
                s = int(supplied) / multiply_decimals(s_decimals) * float(token_price_data[k]["price"])
                supply_farm_apy = handler_decimal((r * 365 / s) * 100, 2)
    return supply_farm_apy


def list_token_data():
    ret_data_list = []
    assets_data_list = get_assets_paged_detailed()["data"]
    extra_decimals = handle_extra_decimals()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    ret_farm_data = {}
    farm_data_list = get_asset_farms_paged()["data"]
    net_tvl_apy = 0
    for farm_data in farm_data_list:
        if "NetTvl" in farm_data:
            for farm in farm_data:
                if "NetTvl" == farm:
                    continue
                else:
                    farm_rewards = farm["rewards"]
                    for reward_token, farm_reward in farm_rewards.items():
                        ret_farm_data[reward_token] = {"reward_per_day": farm_reward["reward_per_day"],
                                                       "boosted_shares": farm_reward["boosted_shares"]}
    if global_config.burrow_token in ret_farm_data:
        reward_per_day = (int(ret_farm_data[global_config.burrow_token]["reward_per_day"]) / multiply_decimals(19)) * float(token_price_data[global_config.burrow_token]["price"]) * 365
        boosted_shares = int(ret_farm_data[global_config.burrow_token]["boosted_shares"]) / multiply_decimals(19)
        net_tvl_apy = reward_per_day / boosted_shares
    for assets_data in assets_data_list:
        token_id = assets_data["token_id"]
        if token_id not in token_price_data:
            continue
        total_supplied_balance = int(assets_data["supplied"]["balance"]) + int(assets_data["reserved"]) + int(
            assets_data["prot_fee"])
        token_decimals = token_price_data[token_id]["decimals"] + assets_data["config"]["extra_decimals"]
        total_supplied_balance = handler_decimal(total_supplied_balance / multiply_decimals(token_decimals), 6)
        total_burrow_balance = handler_decimal(
            int(assets_data["borrowed"]["balance"]) / multiply_decimals(token_decimals), 6)
        borrow_apy = "0.00"
        can_borrow = assets_data["config"]["can_borrow"]
        if can_borrow:
            borrow_apy = handler_decimal(float(assets_data["borrow_apr"]) * 100, 2)
        net_tvl_multiplier = assets_data["config"]["net_tvl_multiplier"]
        if net_tvl_multiplier != 0:
            net_tvl_multiplier = net_tvl_multiplier / 10000
        available_liquidity = float(total_supplied_balance) - float(total_burrow_balance)
        supply_farm_apy = handle_supply_farm_apy(assets_data, token_price_data, extra_decimals)
        ret_data = {
            "token": token_id,
            "symbol": token_price_data[token_id]["symbol"],
            "price": token_price_data[token_id]["price"],
            "base_apy": handler_decimal(float(assets_data["supply_apr"]) * 100, 2),
            "net_liquidity_apy": handler_decimal(float(net_tvl_apy * net_tvl_multiplier) * 100, 2),
            "supply_farm_apy": supply_farm_apy,
            "borrow_apy": borrow_apy,
            "supply_apy": handler_decimal(
                float(assets_data["supply_apr"]) * 100 + float(net_tvl_apy * net_tvl_multiplier) * 100 + float(
                    supply_farm_apy), 2),
            "total_supplied_balance": total_supplied_balance,
            "total_supplied_price": handler_decimal(
                float(total_supplied_balance) * float(token_price_data[token_id]["price"]), 6),
            "total_burrow_balance": total_burrow_balance,
            "total_burrow_price": handler_decimal(
                float(total_burrow_balance) * float(token_price_data[token_id]["price"]), 6),
            "available_liquidity_balance": handler_decimal(available_liquidity - available_liquidity * 0.001, 6),
            "available_liquidity_price": handler_decimal(
                (available_liquidity - available_liquidity * 0.001) * float(token_price_data[token_id]["price"]), 6)
        }
        ret_data_list.append(ret_data)
    return success(ret_data_list)


def deposit(token_id, amount, is_collateral):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_deposit = True
    check_collateral = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_deposit = assets_paged_detailed["config"]["can_deposit"]
            check_collateral = assets_paged_detailed["config"]["can_use_as_collateral"]
    if not check_deposit:
        return error("The token not deposit", "1005")
    burrow_handler = BurrowHandler(signer, token_id)
    if is_collateral:
        if not check_collateral:
            return error("The token not collateral", "1006")
        extra_decimals = handle_extra_decimals()
        max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
        ret = burrow_handler.deposit_collateral(amount, max_amount)
    else:
        ret = burrow_handler.deposit(amount)
    return success(ret)


def deposit_lp(token_id, amount, is_collateral, pool_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_deposit = True
    check_collateral = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_deposit = assets_paged_detailed["config"]["can_deposit"]
            check_collateral = assets_paged_detailed["config"]["can_use_as_collateral"]
    if not check_deposit:
        return error("The token not deposit", "1005")
    burrow_handler = BurrowHandler(signer, global_config.ref_ex)
    if is_collateral:
        if not check_collateral:
            return error("The token not collateral", "1006")
        ret = burrow_handler.shadow_action_collateral(token_id, pool_id)
    else:
        ret = burrow_handler.shadow_action(amount, pool_id)
    return success(ret)


def burrow(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_borrowed = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_borrowed = assets_paged_detailed["config"]["can_borrow"]
    if not check_borrowed:
        return error("The token not burrow", "1004")
    burrow_handler = BurrowHandler(signer, token_id)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.burrow(max_amount)
    return success(ret)


def withdraw(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_withdraw = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_withdraw = assets_paged_detailed["config"]["can_withdraw"]
    if not check_withdraw:
        return error("The token not withdraw", "1007")
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    burrow_handler = BurrowHandler(signer, token_id)
    ret = burrow_handler.withdraw(max_amount)
    return success(ret)


def withdraw_lp(token_id, amount, pool_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_withdraw = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_withdraw = assets_paged_detailed["config"]["can_withdraw"]
    if not check_withdraw:
        return error("The token not withdraw", "1007")
    burrow_handler = BurrowHandler(signer, token_id)
    ret = burrow_handler.withdraw_lp(amount, pool_id)
    return success(ret)


def repay_from_wallet(token_id, amount):
    burrow_handler = BurrowHandler(signer, token_id)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.repay_from_wallet(amount, max_amount)
    return success(ret)


def repay_from_supplied(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.repay_from_supplied(max_amount, token_id)
    return success(ret)


def near_withdraw(amount):
    burrow_handler = BurrowHandler(signer, global_config.near_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_withdraw = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == global_config.near_contract:
            check_withdraw = assets_paged_detailed["config"]["can_withdraw"]
    if not check_withdraw:
        return error("The token not withdraw", "1007")
    ret = burrow_handler.near_withdraw(amount)
    return success(ret)


def increase_collateral(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_collateral = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_collateral = assets_paged_detailed["config"]["can_use_as_collateral"]
    if not check_collateral:
        return error("The token not collateral", "1006")
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.increase_collateral(token_id, max_amount)
    return success(ret)


def decrease_collateral(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_collateral = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_collateral = assets_paged_detailed["config"]["can_use_as_collateral"]
    if not check_collateral:
        return error("The token not collateral", "1006")
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    burrow_handler = BurrowHandler(signer, global_config.priceoracle_contract)
    ret = burrow_handler.decrease_collateral(token_id, max_amount)
    return success(ret)


def get_assets():
    burrow_handler = BurrowHandler(signer, global_config.priceoracle_contract)
    ret = burrow_handler.get_assets()
    return success(ret)


def account_stake_booster(amount, duration):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.account_stake_booster(amount, duration)
    return success(ret)


def account_unstake_booster():
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.account_unstake_booster()
    return success(ret)


def account_farm_claim_all():
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.account_farm_claim_all()
    return success(ret)


def get_extra_decimals_and_volatility_ratio():
    assets_data_list = get_assets_paged_detailed()["data"]
    extra_decimals = {}
    volatility_ratio = {}
    net_tvl_multiplier = {}
    for assets_data in assets_data_list:
        extra_decimals[assets_data["token_id"]] = assets_data["config"]["extra_decimals"]
        volatility_ratio[assets_data["token_id"]] = assets_data["config"]["volatility_ratio"]
        net_tvl_multiplier[assets_data["token_id"]] = assets_data["config"]["net_tvl_multiplier"]
    return extra_decimals, volatility_ratio, net_tvl_multiplier


def get_net_tvl_multiplier_ratio():
    assets_data_list = get_assets_paged_detailed()["data"]
    net_tvl_multiplier = {}
    for assets_data in assets_data_list:
        net_tvl_multiplier[assets_data["token_id"]] = assets_data["config"]["net_tvl_multiplier"]
    return net_tvl_multiplier


def supply_health_factor_trial(account_data):
    max_ratio = 10000
    if account_data is None:
        return 0
    borrowed_data_list = account_data["borrowed"]
    collateral_data_list = account_data["collateral"]
    extra_decimals, volatility_ratio, net_tvl_multiplier = get_extra_decimals_and_volatility_ratio()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    total_borrowed_amount = 0
    total_collateral_amount = 0
    for borrowed_data in borrowed_data_list:
        decimals = token_price_data[borrowed_data["token_id"]]["decimals"] + extra_decimals[borrowed_data["token_id"]]
        total_borrowed_amount += (int(borrowed_data["balance"]) / multiply_decimals(decimals) *
                                  token_price_data[borrowed_data["token_id"]]["price"]) / (
                                             volatility_ratio[borrowed_data["token_id"]] / 10000)
    for collateral_data in collateral_data_list:
        decimals = token_price_data[collateral_data["token_id"]]["decimals"] + extra_decimals[
            collateral_data["token_id"]]
        total_collateral_amount += (int(collateral_data["balance"]) / multiply_decimals(decimals) *
                                    token_price_data[collateral_data["token_id"]]["price"]) * (
                                               volatility_ratio[collateral_data["token_id"]] / 10000)
    if total_borrowed_amount == 0:
        return max_ratio
    if total_collateral_amount == 0:
        return 0
    health_factor_ratio = total_collateral_amount / total_borrowed_amount
    if health_factor_ratio > max_ratio:
        return max_ratio
    else:
        return handler_decimal(health_factor_ratio * 100, 2)


def health_factor(account_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    account_data = burrow_handler.get_account(account_id)
    return success(supply_health_factor_trial(account_data))


def max_supply_balance(account_id, token, is_check_deposit):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_deposit = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_deposit = assets_paged_detailed["config"]["can_deposit"]
    if not check_deposit and is_check_deposit:
        return error("The token not deposit", "1005")
    burrow_handler = BurrowHandler(signer, token)
    ft_balance = burrow_handler.ft_balance_of(account_id)
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    token_decimals = token_price_data[token]["decimals"]
    token_balance = int(ft_balance) / multiply_decimals(token_decimals)
    if token == global_config.near_contract:
        token_balance = token_balance + get_account_near_balance(account_id) - 0.25
    if token_balance < 0:
        token_balance = 0
    else:
        token_balance = handler_decimal(token_balance, 12)
    return success(token_balance)


def max_burrow_balance(account_id, token):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    account_data = burrow_handler.get_account(account_id)
    if account_data is None:
        return success(0)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_borrowed = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_borrowed = assets_paged_detailed["config"]["can_borrow"]
    if not check_borrowed:
        return error("The token not burrow", "1004")
    borrowed_data_list = account_data["borrowed"]
    collateral_data_list = account_data["collateral"]
    extra_decimals, volatility_ratio, net_tvl_multiplier = get_extra_decimals_and_volatility_ratio()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    total_borrowed_amount = 0
    total_collateral_amount = 0
    for borrowed_data in borrowed_data_list:
        token_decimals = token_price_data[borrowed_data["token_id"]]["decimals"] + extra_decimals[borrowed_data["token_id"]]
        total_borrowed_amount += int(borrowed_data["balance"]) / multiply_decimals(token_decimals) * token_price_data[borrowed_data["token_id"]]["price"] / (volatility_ratio[borrowed_data["token_id"]] / 10000)
    for collateral_data in collateral_data_list:
        token_decimals = token_price_data[collateral_data["token_id"]]["decimals"] + extra_decimals[collateral_data["token_id"]]
        total_collateral_amount += int(collateral_data["balance"]) / multiply_decimals(token_decimals) * token_price_data[collateral_data["token_id"]]["price"] * (volatility_ratio[collateral_data["token_id"]] / 10000)
    total_amount_balance = (total_collateral_amount - total_borrowed_amount) * (volatility_ratio[token] / 10000)
    total_amount = total_amount_balance / token_price_data[token]["price"] * 95 / 100
    assets_balance = 0
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            token_decimals = token_price_data[token]["decimals"] + extra_decimals[token]
            assets_balance = (int(assets_paged_detailed["reserved"]) + int(assets_paged_detailed["prot_fee"]) + int(assets_paged_detailed["supplied"]["balance"]) - int(assets_paged_detailed["borrowed"]["balance"])) / multiply_decimals(token_decimals) * 0.999
    ret = min(assets_balance, total_amount)
    return success(ret)


def max_withdraw_balance(account_id, token, is_check_withdraw):
    ret = 0
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_withdraw = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_withdraw = assets_paged_detailed["config"]["can_withdraw"]
    if not check_withdraw and is_check_withdraw:
        return error("The token not withdraw", "1007")
    account_data = burrow_handler.get_account(account_id)
    if account_data is None:
        return success(ret)
    supplied_data_list = account_data["supplied"]
    borrowed_data_list = account_data["borrowed"]
    collateral_data_list = account_data["collateral"]
    extra_decimals, volatility_ratio, net_tvl_multiplier = get_extra_decimals_and_volatility_ratio()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    total_borrowed_amount = 0
    total_collateral_amount = 0
    max_amount = 0
    min_amount = 0
    collateral_balance = 0
    for supplied_data in supplied_data_list:
        if supplied_data["token_id"] == token:
            max_amount = int(supplied_data["balance"]) / multiply_decimals(token_price_data[token]["decimals"] + extra_decimals[token])
    for borrowed_data in borrowed_data_list:
        decimals = token_price_data[borrowed_data["token_id"]]["decimals"] + extra_decimals[borrowed_data["token_id"]]
        total_borrowed_amount += (int(borrowed_data["balance"]) / multiply_decimals(decimals) * token_price_data[borrowed_data["token_id"]]["price"]) / (volatility_ratio[borrowed_data["token_id"]] / 10000)
    for collateral_data in collateral_data_list:
        if collateral_data["token_id"] == token:
            collateral_balance = int(collateral_data["balance"])
        decimals = token_price_data[collateral_data["token_id"]]["decimals"] + extra_decimals[collateral_data["token_id"]]
        total_collateral_amount += (int(collateral_data["balance"]) / multiply_decimals(decimals) * token_price_data[collateral_data["token_id"]]["price"]) * (volatility_ratio[collateral_data["token_id"]] / 10000)
    if collateral_balance > 0:
        adjusted_priced_diff = total_collateral_amount - total_borrowed_amount
        if adjusted_priced_diff < 0:
            safe_diff = 0
        else:
            safe_diff = adjusted_priced_diff * 999 / 1000 / (volatility_ratio[token] / 10000) / token_price_data[token]["price"]
        collateral_balance = collateral_balance / multiply_decimals(token_price_data[token]["decimals"] + extra_decimals[token])
        min_amount = min(collateral_balance, safe_diff)
    ret = max_amount + min_amount
    return success(ret)


def max_adjust_balance(account_id, token):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_collateral = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_collateral = assets_paged_detailed["config"]["can_use_as_collateral"]
    if not check_collateral:
        return error("The token not collateral", "1006")
    account_data = burrow_handler.get_account(account_id)
    if account_data is None:
        return success(0)
    supplied_data_list = account_data["supplied"]
    collateral_data_list = account_data["collateral"]
    extra_decimals, volatility_ratio, net_tvl_multiplier = get_extra_decimals_and_volatility_ratio()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    total_supplied_amount = 0
    total_collateral_amount = 0
    for supplied_data in supplied_data_list:
        if supplied_data["token_id"] == token:
            decimals = token_price_data[supplied_data["token_id"]]["decimals"] + extra_decimals[supplied_data["token_id"]]
            total_supplied_amount += int(supplied_data["balance"]) / multiply_decimals(decimals)
    for collateral_data in collateral_data_list:
        if collateral_data["token_id"] == token:
            decimals = token_price_data[collateral_data["token_id"]]["decimals"] + extra_decimals[collateral_data["token_id"]]
            total_collateral_amount += int(collateral_data["balance"]) / multiply_decimals(decimals)
    ret = total_collateral_amount + total_supplied_amount
    return success(ret)


def max_repay_from_wallet(account_id, token):
    max_supply_data = max_supply_balance(account_id, token, False)
    if max_supply_data["code"] != "0":
        return max_supply_data
    supply_balance = float(max_supply_data["data"])
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    account_data = burrow_handler.get_account(account_id)
    if account_data is None:
        return success(0)
    borrowed_data_list = account_data["borrowed"]
    extra_decimals, volatility_ratio, net_tvl_multiplier = get_extra_decimals_and_volatility_ratio()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    total_borrowed_amount = 0.0
    for borrowed_data in borrowed_data_list:
        if borrowed_data["token_id"] == token:
            token_decimals = token_price_data[borrowed_data["token_id"]]["decimals"] + extra_decimals[borrowed_data["token_id"]]
            total_borrowed_amount += int(borrowed_data["balance"]) / multiply_decimals(token_decimals)
    ret = min(total_borrowed_amount, supply_balance)
    return success(ret)


def max_repay_from_account(account_id, token):
    supply_balance = float(max_withdraw_balance(account_id, token, False)["data"])
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    account_data = burrow_handler.get_account(account_id)
    if account_data is None:
        return success(0)
    borrowed_data_list = account_data["borrowed"]
    extra_decimals, volatility_ratio, net_tvl_multiplier = get_extra_decimals_and_volatility_ratio()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    total_borrowed_amount = 0.0
    for borrowed_data in borrowed_data_list:
        if borrowed_data["token_id"] == token:
            decimals = token_price_data[borrowed_data["token_id"]]["decimals"] + extra_decimals[borrowed_data["token_id"]]
            total_borrowed_amount += int(borrowed_data["balance"]) / multiply_decimals(decimals)
    ret = min(total_borrowed_amount, supply_balance)
    return success(ret)


def account_apy(account_id, token):
    token_data_list = list_token_data()["data"]
    extra_decimals = handle_extra_decimals()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    base_supplied_apy = 0
    base_borrowed_apy = 0
    for token_data in token_data_list:
        if token == token_data["token"]:
            base_supplied_apy = float(token_data["base_apy"])
            base_borrowed_apy = float(token_data["borrow_apy"])
    supplied_apy_data_list = []
    burrowed_apy_data_list = []
    total_supplied_apy = base_supplied_apy
    total_burrowed_apy = base_borrowed_apy
    ret_supplied_apy_data = {
        "base_apy": base_supplied_apy,
        "total_apy": ""
    }
    ret_burrowed_apy_data = {
        "base_apy": base_borrowed_apy,
        "total_apy": ""
    }
    account_data = get_account(account_id)["data"]
    supplied_data_list = account_data["supplied"]
    collateral_data_list = account_data["collateral"]
    borrowed_data_list = account_data["borrowed"]
    total_supplied_amount = 0
    total_collateral_amount = 0
    for supplied_data in supplied_data_list:
        if supplied_data["token_id"] == token:
            decimals = token_price_data[supplied_data["token_id"]]["decimals"] + extra_decimals[
                supplied_data["token_id"]]
            total_supplied_amount += (int(supplied_data["balance"]) / multiply_decimals(decimals) *
                                      token_price_data[supplied_data["token_id"]]["price"])
    for collateral_data in collateral_data_list:
        if collateral_data["token_id"] == token:
            decimals = token_price_data[collateral_data["token_id"]]["decimals"] + extra_decimals[
                collateral_data["token_id"]]
            total_collateral_amount += (int(collateral_data["balance"]) / multiply_decimals(decimals) *
                                        token_price_data[collateral_data["token_id"]]["price"])
    total_amount = total_collateral_amount + total_supplied_amount
    total_borrowed_amount = 0
    for borrowed_data in borrowed_data_list:
        if borrowed_data["token_id"] == token:
            decimals = token_price_data[borrowed_data["token_id"]]["decimals"] + extra_decimals[borrowed_data["token_id"]]
            total_borrowed_amount += (int(borrowed_data["balance"]) / multiply_decimals(decimals) *
                                      token_price_data[borrowed_data["token_id"]]["price"])
    farms = account_data["farms"]
    for farm in farms:
        if "Supplied" in farm["farm_id"] and farm["farm_id"]["Supplied"] == token:
            for reward in farm["rewards"]:
                reward_token_id = reward["reward_token_id"]
                asset_farm_reward = reward["asset_farm_reward"]
                token_balance = int(reward["boosted_shares"]) / int(asset_farm_reward["boosted_shares"]) * int(asset_farm_reward["reward_per_day"])
                decimals = token_price_data[reward_token_id]["decimals"] + extra_decimals[reward_token_id]
                reward_amount = int(token_balance) / multiply_decimals(decimals) * float(token_price_data[reward_token_id]["price"]) * 365
                your_apy = reward_amount / total_amount * 100
                supplied_apy_data = {"token": reward_token_id, "your_apy": handler_decimal(your_apy, 2)}
                supplied_apy_data_list.append(supplied_apy_data)
                total_supplied_apy = total_supplied_apy + your_apy
        if "Borrowed" in farm["farm_id"] and farm["farm_id"]["Borrowed"] == token:
            for reward in farm["rewards"]:
                reward_token_id = reward["reward_token_id"]
                asset_farm_reward = reward["asset_farm_reward"]
                token_balance = int(reward["boosted_shares"]) / int(asset_farm_reward["boosted_shares"]) * int(asset_farm_reward["reward_per_day"])
                decimals = token_price_data[reward_token_id]["decimals"] + extra_decimals[reward_token_id]
                reward_amount = int(token_balance) / multiply_decimals(decimals) * float(token_price_data[reward_token_id]["price"]) * 365
                your_apy = reward_amount / total_borrowed_amount * 100
                burrowed_apy_data = {"token": reward_token_id, "your_apy": "-" + handler_decimal(your_apy, 2)}
                burrowed_apy_data_list.append(burrowed_apy_data)
                total_burrowed_apy = total_burrowed_apy - your_apy
    ret_supplied_apy_data["your_apy_data"] = supplied_apy_data_list
    ret_burrowed_apy_data["your_apy_data"] = burrowed_apy_data_list
    ret_supplied_apy_data["total_apy"] = handler_decimal(total_supplied_apy, 2)
    ret_burrowed_apy_data["total_apy"] = handler_decimal(total_burrowed_apy, 2)
    ret = {
        "supplied_apy": ret_supplied_apy_data,
        "borrowed_apy": ret_burrowed_apy_data
    }
    return success(ret)


def supply_health_factor(token, account_id, amount, adjust_flag):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_deposit = True
    check_collateral = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_deposit = assets_paged_detailed["config"]["can_deposit"]
            check_collateral = assets_paged_detailed["config"]["can_use_as_collateral"]
    if not check_deposit:
        return error("The token not deposit", "1005")
    if not check_collateral:
        return error("The token not collateral", "1006")
    return supply_and_collateral_health_factor(token, account_id, amount, adjust_flag, burrow_handler)


def collateral_health_factor(token, account_id, amount, adjust_flag):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_collateral = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_collateral = assets_paged_detailed["config"]["can_use_as_collateral"]
    if not check_collateral:
        return error("The token not collateral", "1006")
    return supply_and_collateral_health_factor(token, account_id, amount, adjust_flag, burrow_handler)


def supply_and_collateral_health_factor(token, account_id, amount, adjust_flag, burrow_handler):
    account_data = burrow_handler.get_account(account_id)
    extra_decimals = handle_extra_decimals()
    collateral_data_list = account_data["collateral"]
    token_flag = True
    for collateral_data in collateral_data_list:
        if collateral_data["token_id"] == token:
            token_flag = False
            if adjust_flag:
                collateral_data["balance"] = int(collateral_data["balance"]) + (
                            float(amount) * multiply_decimals(extra_decimals[token]))
            else:
                collateral_data["balance"] = int(collateral_data["balance"]) - (
                            float(amount) * multiply_decimals(extra_decimals[token]))
    if token_flag:
        collateral_new_data = {
            "apr": "0",
            "balance": (float(amount) * multiply_decimals(extra_decimals[token])),
            "shares": (float(amount) * multiply_decimals(extra_decimals[token])),
            "token_id": token
        }
        account_data["collateral"].append(collateral_new_data)
    return success(supply_health_factor_trial(account_data))


def supply_not_collateral_health_factor(account_id, token_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_deposit = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token_id:
            check_deposit = assets_paged_detailed["config"]["can_deposit"]
    if not check_deposit:
        return error("The token not deposit", "1005")
    account_data = burrow_handler.get_account(account_id)
    return success(supply_health_factor_trial(account_data))


def burrow_health_factor(token, account_id, amount, adjust_flag):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_borrowed = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_borrowed = assets_paged_detailed["config"]["can_borrow"]
    if not check_borrowed and adjust_flag:
        return error("The token not burrow", "1004")
    account_data = burrow_handler.get_account(account_id)
    extra_decimals = handle_extra_decimals()
    borrowed_data_list = account_data["borrowed"]
    token_flag = True
    for borrowed_data in borrowed_data_list:
        if borrowed_data["token_id"] == token:
            token_flag = False
            if adjust_flag:
                borrowed_data["balance"] = int(borrowed_data["balance"]) + (float(amount) * multiply_decimals(extra_decimals[token]))
            else:
                borrowed_data["balance"] = int(borrowed_data["balance"]) - (float(amount) * multiply_decimals(extra_decimals[token]))
    if token_flag:
        borrowed_new_data = {
            "apr": "0",
            "balance": (float(amount) * multiply_decimals(extra_decimals[token])),
            "shares": (float(amount) * multiply_decimals(extra_decimals[token])),
            "token_id": token
        }
        account_data["borrowed"].append(borrowed_new_data)
    return success(supply_health_factor_trial(account_data))


def withdraw_health_factor(token, account_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    assets_paged_detailed_list = burrow_handler.get_assets_paged_detailed()
    check_withdraw = True
    for assets_paged_detailed in assets_paged_detailed_list:
        if assets_paged_detailed["token_id"] == token:
            check_withdraw = assets_paged_detailed["config"]["can_withdraw"]
    if not check_withdraw:
        return error("The token not withdraw", "1007")
    account_data = burrow_handler.get_account(account_id)
    extra_decimals = handle_extra_decimals()
    withdraw_amount_balance = float(amount) * multiply_decimals(extra_decimals[token])
    withdraw_collateral_balance = 0
    supplied_balance = 0
    supplied_data_list = account_data["supplied"]
    for supplied_data in supplied_data_list:
        if supplied_data["token_id"] == token:
            supplied_balance = int(supplied_data["balance"])
    if withdraw_amount_balance > supplied_balance:
        withdraw_collateral_balance = withdraw_amount_balance - supplied_balance
    collateral_data_list = account_data["collateral"]
    for collateral_data in collateral_data_list:
        if collateral_data["token_id"] == token:
            collateral_data["balance"] = int(collateral_data["balance"]) - withdraw_collateral_balance
    return success(supply_health_factor_trial(account_data))


def repay_from_account_health_factor(token, account_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    account_data = burrow_handler.get_account(account_id)
    extra_decimals = handle_extra_decimals()
    withdraw_amount_balance = float(amount) * multiply_decimals(extra_decimals[token])
    supplied_balance = 0
    supplied_data_list = account_data["supplied"]
    for supplied_data in supplied_data_list:
        if supplied_data["token_id"] == token:
            supplied_balance = int(supplied_data["balance"])
    borrowed_data_list = account_data["borrowed"]
    for borrowed_data in borrowed_data_list:
        if borrowed_data["token_id"] == token:
            borrowed_data["balance"] = int(borrowed_data["balance"]) - (float(amount) * multiply_decimals(extra_decimals[token]))
    collateral_data_list = account_data["collateral"]
    for collateral_data in collateral_data_list:
        if collateral_data["token_id"] == token:
            new_collateral_balance = int(collateral_data["balance"]) + supplied_balance - withdraw_amount_balance
            if int(collateral_data["balance"]) > new_collateral_balance:
                collateral_data["balance"] = new_collateral_balance
    return success(supply_health_factor_trial(account_data))


def check_claim_rewards(account_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    account_data = burrow_handler.get_account(account_id)
    has_non_farmed_assets = account_data["has_non_farmed_assets"]
    supplied_data_list = account_data["supplied"]
    borrowed_data_list = account_data["borrowed"]
    collateral_data_list = account_data["collateral"]
    extra_decimals, volatility_ratio, net_tvl_multiplier = get_extra_decimals_and_volatility_ratio()
    price_data_list = get_price_data()["data"]
    token_price_data = handle_token_price(price_data_list)
    total_supplied_amount = 0
    total_borrowed_amount = 0
    total_collateral_amount = 0
    for supplied_data in supplied_data_list:
        decimals = token_price_data[supplied_data["token_id"]]["decimals"] + extra_decimals[supplied_data["token_id"]]
        total_supplied_amount += (int(supplied_data["balance"]) / multiply_decimals(decimals) *
                                  token_price_data[supplied_data["token_id"]]["price"]) / (
                                             net_tvl_multiplier[supplied_data["token_id"]] / 10000)
    for borrowed_data in borrowed_data_list:
        decimals = token_price_data[borrowed_data["token_id"]]["decimals"] + extra_decimals[borrowed_data["token_id"]]
        total_borrowed_amount += (int(borrowed_data["balance"]) / multiply_decimals(decimals) *
                                  token_price_data[borrowed_data["token_id"]]["price"]) / (
                                             net_tvl_multiplier[borrowed_data["token_id"]] / 10000)
    for collateral_data in collateral_data_list:
        decimals = token_price_data[collateral_data["token_id"]]["decimals"] + extra_decimals[collateral_data["token_id"]]
        total_collateral_amount += (int(collateral_data["balance"]) / multiply_decimals(decimals) *
                                    token_price_data[collateral_data["token_id"]]["price"]) * (
                                               net_tvl_multiplier[collateral_data["token_id"]] / 10000)
    has_negative_net_liquidity = (total_collateral_amount + total_supplied_amount - total_borrowed_amount) < 0
    if not has_non_farmed_assets or has_negative_net_liquidity:
        return success(False)
    else:
        return success(True)


def get_account_all_positions(account_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_account_all_positions(account_id)
    return success(ret)


def get_config():
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_config()
    return success(ret)


def get_unit_lpt_assets(contract_id, pool_ids):
    burrow_handler = BurrowHandler(signer, contract_id)
    ret = burrow_handler.get_unit_lpt_assets(pool_ids)
    return success(ret)


def get_pool_shares(contract_id, account_id, pool_id):
    burrow_handler = BurrowHandler(signer, contract_id)
    ret = burrow_handler.get_pool_shares(account_id, pool_id)
    return success(ret)


def get_shadow_records(contract_id, account_id):
    burrow_handler = BurrowHandler(signer, contract_id)
    ret = burrow_handler.get_shadow_records(account_id)
    return success(ret)


if __name__ == "__main__":
    print("############START###########")
    # a = [{"alarmType":"PRICE_ZERO","source":"coingecko","coin":"wrap.near","extraMsg":"{\"coingecko\":0,\"binance\":1.928,\"binanceFutures\":1.93,\"huobi\":1.9295,\"cryptocom\":null,\"kucoin\":1.9293,\"gate\":1.928,\"chainlink\":0}","startTime":"2023-11-21T07:14:49.374Z"}]
    # b = json.dumps(a)
    # print(b)

    # r = max_withdraw_balance("ae03d71382e8621650adfb5706ca430676d9756893b08c1efeae37c92024ef1a", "a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near")
    # print("ret:", r)

    # r = max_adjust_balance("ae03d71382e8621650adfb5706ca430676d9756893b08c1efeae37c92024ef1a", "wrap.near")
    # print(r)

    # r = list_token_data()
    # print(r)
    # r = account_apy("juaner1.testnet", "token.1689937928.burrow.testnet")
    # print(r)

    # r = repay_from_account_health_factor("usdc.fakes.testnet", "juaner1.testnet", "756000000")
    # print(r)

    # r = max_burrow_balance("juaner1.testnet", "usdc.fakes.testnet")
    # print(r)

    # r = max_withdraw_balance("juaner1.testnet", "ref.fakes.testnet")
    # print(r)

    # r = repay_from_wallet("juaner1.testnet", "usdc.fakes.testnet")
    # print(r)

    # r = get_account_near_balance("juaner1.testnet")
    # print(r)

    # r = max_supply_balance("juaner1.testnet", "wrap.testnet")
    # print(r)

    r = check_claim_rewards("juaner.near")
    print(r)

    # r = supply_health_factor("meta-token.near", "juaner.near", "10000000", True)
    # print(r)

