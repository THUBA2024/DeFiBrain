import json
from config import GlobalConfig
global_config = GlobalConfig()


class BurrowHandler:
    def __init__(self, signer, contract_id):
        self._signer = signer
        self._contract_id = contract_id

    def storage_balance_of(self, account_id: str):
        return self._signer.view_function(
            self._contract_id,
            "storage_balance_of",
            {
                "account_id": account_id,
            }
        )['result']

    def get_assets_paged_detailed(self):
        return self._signer.view_function(
            self._contract_id,
            "get_assets_paged_detailed",
            {
                "from_index": 0,
                "limit": 100
            }
        )['result']

    def get_asset_farms_paged(self):
        return self._signer.view_function(
            self._contract_id,
            "get_asset_farms_paged",
            {
                "from_index": 0,
                "limit": 100
            }
        )['result']

    def get_account(self, account_id: str):
        return self._signer.view_function(
            self._contract_id,
            "get_account",
            {
                "account_id": account_id
            }
        )['result']

    def get_price_data(self):
        return self._signer.view_function(
            self._contract_id,
            "get_price_data",
            {
            }
        )['result']

    def ft_metadata(self):
        return self._signer.view_function(
            self._contract_id,
            "ft_metadata",
            {
            }
        )['result']

    def deposit(self, amount: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "msg": ""
            },
            "amount": global_config.deposit_yocto
        }

    def deposit_collateral(self, amount: str, max_amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "IncreaseCollateral": {
                        "token_id": self._contract_id,
                        "max_amount": max_amount
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def burrow(self, amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "Borrow": {
                        "token_id": self._contract_id,
                        "amount": amount
                    }
                }, {
                    "Withdraw": {
                        "token_id": self._contract_id,
                        "max_amount": amount
                    }
                }]
            }
        }
        return {
            "contract_id": global_config.priceoracle_contract,
            "method_name": "oracle_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def near_withdraw(self, amount: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "near_withdraw",
            "args": {
                "amount": amount
            },
            "amount": global_config.deposit_yocto
        }

    def withdraw(self, amount: str):
        return {
            "contract_id": global_config.burrow_contract,
            "method_name": "execute",
            "args": {
                "actions": [
                    {
                        "Withdraw": {
                            "token_id": self._contract_id,
                            "max_amount": amount
                        }
                    }
                ]
            },
            "amount": global_config.deposit_yocto
        }

    def repay_from_wallet(self, amount: str, max_amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "Repay": {
                        "max_amount": max_amount,
                        "token_id": self._contract_id,
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def repay_from_supplied(self, amount: str, contract_id: str):
        return {
            "contract_id": global_config.burrow_contract,
            "method_name": "execute",
            "args": {
                "actions": [
                    {
                        "Repay": {
                            "token_id": contract_id,
                            "max_amount": amount
                        }
                    }
                ]
            },
            "amount": global_config.deposit_yocto
        }

    def storage_deposit(self, account_id: str, amount: float):
        return {
            "contract_id": self._contract_id,
            "method_name": "storage_deposit",
            "args": {
                "account_id": account_id
            },
            "amount": amount
        }

    def decrease_collateral(self, token_id: str, amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "DecreaseCollateral": {
                        "token_id": token_id,
                        "max_amount": amount
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "oracle_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def increase_collateral(self, token_id: str, amount: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "execute",
            "args": {
                "actions": [{
                    "IncreaseCollateral": {
                        "token_id": token_id,
                        "max_amount": amount
                    }
                }]
            },
            "amount": global_config.deposit_yocto
        }

    def get_assets(self):
        return self._signer.view_function(
            self._contract_id,
            "get_asset",
            {
                "asset_id": "usdt.tether-token.near"
            }
        )['result']

    def ft_balance_of(self, account_id):
        return self._signer.view_function(
            self._contract_id,
            "ft_balance_of",
            {
                "account_id": account_id
            }
        )['result']

    def account_stake_booster(self, amount: str, duration: int):
        return {
            "contract_id": self._contract_id,
            "method_name": "account_stake_booster",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "duration": duration
            },
        }

    def account_unstake_booster(self):
        return {
            "contract_id": self._contract_id,
            "method_name": "account_unstake_booster",
            "args": {
                "receiver_id": global_config.burrow_contract
            },
        }

    def account_farm_claim_all(self):
        return {
            "contract_id": self._contract_id,
            "method_name": "account_farm_claim_all",
            "args": None,
        }

    def get_account_all_positions(self, account_id: str):
        return self._signer.view_function(
            self._contract_id,
            "get_account_all_positions",
            {
                "account_id": account_id
            }
        )['result']

    def get_config(self):
        return self._signer.view_function(
            self._contract_id,
            "get_config",
            {
            }
        )['result']

    def get_unit_lpt_assets(self, pool_ids: list):
        return self._signer.view_function(
            self._contract_id,
            "get_unit_lpt_assets",
            {
                "pool_ids": pool_ids
            }
        )['result']

    def get_pool_shares(self, account_id: str, pool_id: int):
        return self._signer.view_function(
            self._contract_id,
            "get_pool_shares",
            {
                "account_id": account_id,
                "pool_id": pool_id
            }
        )['result']

    def get_shadow_records(self, account_id: str):
        return self._signer.view_function(
            self._contract_id,
            "get_shadow_records",
            {
                "account_id": account_id
            }
        )['result']

    def shadow_action(self, amount: str, pool_id: int):
        ret = {
            "contract_id": self._contract_id,
            "method_name": "shadow_action",
            "args": {
                "action": "ToBurrowland",
                "pool_id": pool_id,
                "msg": ""
            },
            "amount": global_config.deposit_yocto
        }
        if amount != "":
            ret["args"]["amount"] = amount
        return ret

    def shadow_action_collateral(self, token_id: str, pool_id: int):
        msg = {
            "Execute": {
                "actions": [{
                    "PositionIncreaseCollateral": {
                        "position": token_id,
                        "asset_amount": {
                            "token_id": token_id
                        }
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "action": "ToBurrowland",
                "pool_id": pool_id,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def withdraw_lp(self, amount: str, pool_id: int):
        ret = {
            "contract_id": self._contract_id,
            "method_name": "shadow_action",
            "args": {
                "action": "FromBurrowland",
                "pool_id": pool_id,
                "msg": ""
            },
            "amount": global_config.deposit_yocto
        }
        if amount != "":
            ret["args"]["amount"] = amount
        return ret

