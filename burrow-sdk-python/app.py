#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import request
from burrow.burrow_handler import storage_balance_of, get_assets_paged_detailed, get_asset_farms_paged, get_account, \
    get_price_data, list_token_data, deposit, burrow, withdraw, repay_from_wallet, repay_from_supplied, \
    storage_deposit, near_withdraw, increase_collateral, decrease_collateral, send_message, account_stake_booster, \
    account_unstake_booster, account_farm_claim_all, health_factor, max_supply_balance, max_burrow_balance, \
    max_withdraw_balance, max_adjust_balance, max_repay_from_wallet, max_repay_from_account, account_apy, \
    supply_health_factor, burrow_health_factor, repay_from_account_health_factor, withdraw_health_factor, \
    check_claim_rewards, supply_not_collateral_health_factor, collateral_health_factor, get_account_all_positions, \
    get_config, get_unit_lpt_assets, get_pool_shares, get_shadow_records, deposit_lp, withdraw_lp
import logging
from burrow.tool_util import error, is_number
from burrow.circulating_supply import update_marketcap, get_circulating_supply
from loguru import logger


service_version = "20240221.01"
Welcome = 'Welcome to burrow SDK API server, ' + service_version
app = Flask(__name__)


@app.route('/')
def hello_world():
    return Welcome


@app.route('/storage_balance_of', methods=['POST'])
def handle_storage_balance_of():
    try:
        request_data = request.get_json()
        account_id = request_data["account_id"]
        token_id = request_data["token_id"]
    except Exception as e:
        return error("The required field is empty", "1002")
    try:
        return storage_balance_of(account_id, token_id)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/storage_deposit', methods=['POST'])
def handle_storage_deposit():
    try:
        request_data = request.get_json()
        account_id = request_data["account_id"]
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    try:
        return storage_deposit(account_id, token_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_assets_paged_detailed', methods=['GET'])
def handle_get_assets_paged():
    try:
        return get_assets_paged_detailed()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_asset_farms_paged', methods=['GET'])
def handle_get_asset_farms_paged():
    try:
        return get_asset_farms_paged()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_account/<account_id>', methods=['GET'])
def handle_get_account(account_id):
    try:
        return get_account(account_id)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_price_data', methods=['GET'])
def handle_get_price_data():
    try:
        return get_price_data()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/list_token_data', methods=['GET'])
def handle_list_token_dta():
    try:
        return list_token_data()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/supply', methods=['POST'])
def handle_supply():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        is_collateral = request_data["is_collateral"]
        pool_id = ""
        if "pool_id" in request_data:
            pool_id = request_data["pool_id"]
        amount = ""
        if "amount" in request_data:
            amount = request_data["amount"]
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "" or is_collateral is None or is_collateral == "":
        return error("The required field is empty", "1002")
    try:
        if token_id.startswith("shadow_ref_v1-"):
            if not is_number(pool_id):
                return error("The pool_id incorrect", "1008")
            return deposit_lp(token_id, amount, is_collateral, pool_id)
        else:
            if not is_number(amount):
                return error("Amount Non numeric", "1003")
            return deposit(token_id, amount, is_collateral)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/burrow', methods=['POST'])
def handle_burrow():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return burrow(token_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/withdraw', methods=['POST'])
def handle_withdraw():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        pool_id = ""
        if "pool_id" in request_data:
            pool_id = request_data["pool_id"]
        amount = ""
        if "amount" in request_data:
            amount = request_data["amount"]
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        if token_id.startswith("shadow_ref_v1-"):
            if not is_number(pool_id):
                return error("The pool_id incorrect", "1008")
            return withdraw_lp(token_id, amount, pool_id)
        else:
            if not is_number(amount):
                return error("Amount Non numeric", "1003")
            return withdraw(token_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_wallet', methods=['POST'])
def handle_repay_from_wallet():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return repay_from_wallet(token_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_supplied', methods=['POST'])
def handle_repay_from_supplied():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return repay_from_supplied(token_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/near_withdraw', methods=['POST'])
def handle_near_withdraw():
    try:
        request_data = request.get_json()
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if amount is None or amount == "":
        return error("The required field is empty", "1002")
    try:
        return near_withdraw(amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/increase_collateral', methods=['POST'])
def handle_increase_collateral():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return increase_collateral(token_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/decrease_collateral', methods=['POST'])
def handle_decrease_collateral():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return decrease_collateral(token_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/send_message', methods=['POST'])
def handle_send_message():
    try:
        request_data = request.get_json()
        message = request_data["message"]
        return send_message(message)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/v1/circulating-supply', methods=['GET'])
def handle_circulating_supply():
    try:
        return update_marketcap()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/v2/circulating_supply', methods=['GET'])
def handle_get_circulating_supply():
    try:
        return str(get_circulating_supply())
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/total_supply', methods=['GET'])
def handle_total_supply():
    try:
        return str(1000000000)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_stake_booster', methods=['POST'])
def handle_account_stake_booster():
    try:
        request_data = request.get_json()
        amount = request_data["amount"]
        duration = request_data["duration"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    try:
        return account_stake_booster(amount, duration)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_unstake_booster', methods=['POST'])
def handle_account_unstake_booster():
    try:
        return account_unstake_booster()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_farm_claim_all', methods=['POST'])
def handle_account_farm_claim_all():
    try:
        return account_farm_claim_all()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/health_factor/<account_id>', methods=['GET'])
def handle_health_factor(account_id):
    try:
        return health_factor(account_id)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_supply_balance/<account_id>/<token>', methods=['GET'])
def handle_max_supply_balance(account_id, token):
    try:
        return max_supply_balance(account_id, token, True)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_burrow_balance/<account_id>/<token>', methods=['GET'])
def handle_max_burrow_balance(account_id, token):
    try:
        return max_burrow_balance(account_id, token)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_withdraw_balance/<account_id>/<token>', methods=['GET'])
def handle_max_withdraw_balance(account_id, token):
    try:
        return max_withdraw_balance(account_id, token, True)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_adjust_balance/<account_id>/<token>', methods=['GET'])
def handle_max_adjust_balance(account_id, token):
    try:
        return max_adjust_balance(account_id, token)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_repay_from_wallet/<account_id>/<token>', methods=['GET'])
def handle_max_repay_from_wallet(account_id, token):
    try:
        return max_repay_from_wallet(account_id, token)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_repay_from_account/<account_id>/<token>', methods=['GET'])
def handle_max_repay_from_account(account_id, token):
    try:
        return max_repay_from_account(account_id, token)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_apy/<account_id>/<token>', methods=['GET'])
def handle_account_apy(account_id, token):
    try:
        return account_apy(account_id, token)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/supply_health_factor', methods=['POST'])
def handle_supply_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        is_collateral = request_data["is_collateral"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "" or is_collateral is None or is_collateral == "":
        return error("The required field is empty", "1002")
    try:
        if is_collateral:
            ret = supply_health_factor(token_id, account_id, amount, True)
        else:
            ret = supply_not_collateral_health_factor(account_id, token_id)
        return ret
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/burrow_health_factor', methods=['POST'])
def handle_burrow_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return burrow_health_factor(token_id, account_id, amount, True)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/increase_collateral_health_factor', methods=['POST'])
def handle_increase_collateral_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return collateral_health_factor(token_id, account_id, amount, True)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/decrease_collateral_health_factor', methods=['POST'])
def handle_decrease_collateral_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return collateral_health_factor(token_id, account_id, amount, False)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/withdraw_health_factor', methods=['POST'])
def handle_withdraw_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return withdraw_health_factor(token_id, account_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_wallet_health_factor', methods=['POST'])
def handle_repay_from_wallet_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return burrow_health_factor(token_id, account_id, amount, False)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_account_health_factor', methods=['POST'])
def handle_repay_from_account_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        return repay_from_account_health_factor(token_id, account_id, amount)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/check_claim_rewards/<account_id>', methods=['GET'])
def handle_check_claim_rewards(account_id):
    try:
        return check_claim_rewards(account_id)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_account_all_positions/<account_id>', methods=['GET'])
def handle_get_account_all_positions(account_id):
    try:
        return get_account_all_positions(account_id)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_config', methods=['GET'])
def handle_get_config():
    try:
        return get_config()
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_unit_lpt_assets', methods=['POST'])
def handle_get_unit_lpt_assets():
    try:
        request_data = request.get_json()
        contract_id = request_data["contract_id"]
        pool_ids = request_data["pool_ids"]
    except Exception as e:
        return error("The required field is empty", "1002")
    if contract_id is None or contract_id == "" or pool_ids is None or pool_ids == "":
        return error("The required field is empty", "1002")
    try:
        return get_unit_lpt_assets(contract_id, pool_ids)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_pool_shares', methods=['POST'])
def handle_get_pool_shares():
    try:
        request_data = request.get_json()
        contract_id = request_data["contract_id"]
        account_id = request_data["account_id"]
        pool_id = request_data["pool_id"]
    except Exception as e:
        return error("The required field is empty", "1002")
    if contract_id is None or contract_id == "" or pool_id is None or pool_id == "" or account_id is None or account_id == "":
        return error("The required field is empty", "1002")
    try:
        return get_pool_shares(contract_id, account_id, pool_id)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_shadow_records', methods=['POST'])
def handle_get_shadow_records():
    try:
        request_data = request.get_json()
        contract_id = request_data["contract_id"]
        account_id = request_data["account_id"]
    except Exception as e:
        return error("The required field is empty", "1002")
    if contract_id is None or contract_id == "" or account_id is None or account_id == "":
        return error("The required field is empty", "1002")
    try:
        return get_shadow_records(contract_id, account_id)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


logger.add("burrow.log")
if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.logger.info(Welcome)
    app.run(host='0.0.0.0', port=8100, debug=False)
