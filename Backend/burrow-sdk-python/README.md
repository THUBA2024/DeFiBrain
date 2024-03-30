## Response Code List

| Response Code | Description                 |
| ------------- | --------------------------- |
| 0             | Successful API call         |
| 1001          | Contract call exception     |
| 1002          | The required field is empty |
| 1003          | Amount Non numeric    |
| 1004          | The token not burrow    |
| 1005          | The token not deposit    |
| 1006          | The token not collateral    |
| 1007          | The token not withdraw    |
| 1008          | The pool_id incorrect    |

**Note**: For all inputs involving amounts, the amount should be entered with decimal precision as per the decimal precision in the metadata.

---

## NETWORK
- **TEST_URL**:https://test-api.burrow.finance
- **PROD_URL**:https://api.burrow.finance

---

## It is recommended to deploy the service on your own, and the deployment method is as follows
### 1. clone code
```
git clone https://github.com/burrowHQ/burrow-sdk-python.git
```
### 2. Creating a virtual environment(Enter the cloned code path first, and then execute the command to create a virtual environment)
```
python -m venv venv
```
### 4. Entering the virtual environment
```
. ./venv/bin/activate
```
### 5. Installation dependencies
```
pip install -r requirements.txt
```
### 6. Start Service
```
sh start_server.sh
```

---

## 1. Account Query

- **Test Interface URL**: [https://test-api.burrow.finance/storage_balance_of](https://test-api.burrow.finance/storage_balance_of)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description            |
| ---------- | ---------- | ---------------------- |
| token_id   | String     | Contract address       |
| account_id | String     | Account to be queried  |

**Sample Call**:

```
{
  "token_id": "contract.main.burrow.near",
  "account_id": "account.near"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "available": "150000000000000000000000",
    "total": "250000000000000000000000"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Storage fees for the current account           |

---

## 2. Account Registration

- **Test Interface URL**: [https://test-api.burrow.finance/storage_deposit](https://test-api.burrow.finance/storage_deposit)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                     |
| ---------- | ---------- | ----------------------------------------------- |
| token_id   | String     | Contract address                                |
| account_id | String     | Account to be queried                           |
| amount     | String     | Storage fee in yoctoNear, as per burrow contract |

**Sample Call**:

```
{
  "account_id": "dom1.near",
  "token_id": "contract.main.burrow.near",
  "amount": 1
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "account_id": "dom1.near"
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "storage_deposit"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Parameters of the contract call                |


## 3. Token Asset List

- **Test Interface URL**: [https://test-api.burrow.finance/get_assets_paged_detailed](https://test-api.burrow.finance/get_assets_paged_detailed)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": [
    {
      "borrow_apr": "0.0",
      "borrowed": {
        "balance": "0",
        "shares": "0"
      },
      ...
      "token_id": "token.burrow.near"
    },
    ...
  ],
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Successful return of token asset list          |


## 4. Farms List

- **Test Interface URL**: [https://test-api.burrow.finance/get_asset_farms_paged](https://test-api.burrow.finance/get_asset_farms_paged)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": [
    [
      {
        "Supplied": "token.burrow.near"
      },
      {
        "block_timestamp": "1700208807839905264",
        "rewards": {
          "token.burrow.near": {
            "boosted_shares": "255113043332545463643545574",
            "booster_log_base": "0",
            "remaining_rewards": "177511740235341250000406",
            "reward_per_day": "12000000000000000000000"
          }
        }
      }
    ]
  ],
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Successful return of farm list                 |

---

## 5. Account Asset Details

- **Test Interface URL**: [https://test-api.burrow.finance/get_account/juaner.near](https://test-api.burrow.finance/get_account/juaner.near)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "account_id": "juaner.near",
    "booster_staking": {
      "staked_booster_amount": "10000000000000000000",
      "unlock_timestamp": "1702705309123136860",
      "x_booster_amount": "10000000000000000000"
    },
    "borrowed": [{
      "apr": "0.020115787307602972732631807",
      "balance": "2000063444139612355115550",
      "shares": "1824204883064976309651628",
      "token_id": "wrap.near"
    }],
    ...
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Current account's asset balance in the contract |


## 6. Price Query

- **Test Interface URL**: [https://test-api.burrow.finance/get_price_data](https://test-api.burrow.finance/get_price_data)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "prices": [
      {
        "asset_id": "wrap.near",
        "price": {
          "decimals": 28,
          "multiplier": "18900"
        }
      },
      {
        "asset_id": "c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2.factory.bridge.near",
        "price": null
      },
      ...
    ],
    "recency_duration_sec": 90,
    "timestamp": "1700211816385474579"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Token price list                               |

---

## 7. Token Analysis Data List

- **Test Interface URL**: [https://test-api.burrow.finance/list_token_data](https://test-api.burrow.finance/list_token_data)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": [
    {
      "available_liquidity_balance": "262203363.455576",
      "available_liquidity_price": "103140.315049",
      "base_apy": "0.00",
      "borrow_apy": "0.00",
      "net_liquidity_apy": "1.85",
      "price": "0.00039336",
      "supply_apy": "3.52",
      "supply_farm_apy": "1.67",
      "symbol": "BRRR",
      "token": "token.burrow.near",
      ...
    },
    ...
  ],
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Token information data list                    |


## 8. Supply

- **Test Interface URL**: [https://test-api.burrow.finance/supply](https://test-api.burrow.finance/supply)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                             |
| ------------- | ---------- | --------------------------------------- |
| token_id      | String     | Token to operate on                     |
| amount        | String     | Supply amount, precision as per metadata|
| is_collateral | Boolean    | Whether to use as collateral            |

**Sample Call**:

```
{
  "token_id": "a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near",
  "amount": "1000000",
  "is_collateral": true
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "amount": "1000000",
      "msg": "{\"Execute\": {\"actions\": [{\"IncreaseCollateral\": {\"token_id\": \"a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near\", \"max_amount\": \"1000000000000000000\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near",
    "method_name": "ft_transfer_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |

---

## 9. Burrow

- **Test Interface URL**: [https://test-api.burrow.finance/burrow](https://test-api.burrow.finance/burrow)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Burrow amount, precision as per metadata  |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "1": 1,
    "args": {
      "msg": "{\"Execute\": {\"actions\": [{\"Borrow\": {\"token_id\": \"wrap.near\", \"amount\": \"1\"}}, {\"Withdraw\": {\"token_id\": \"wrap.near\", \"max_amount\": \"1\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "priceoracle.near",
    "method_name": "oracle_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |


## 10. Withdraw

- **Test Interface URL**: [https://test-api.burrow.finance/withdraw](https://test-api.burrow.finance/withdraw)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Withdrawal amount, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "actions": [
        {
          "Withdraw": {
            "max_amount": "1",
            "token_id": "wrap.near"
          }
        }
      ]
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "execute"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |

---

## 11. Repay from Wallet

- **Test Interface URL**: [https://test-api.burrow.finance/repay_from_wallet](https://test-api.burrow.finance/repay_from_wallet)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Repayment amount, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "amount": "1",
      "msg": "{\"Execute\": {\"actions\": [{\"Repay\": {\"max_amount\": \"1000000000000\", \"token_id\": \"17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1",
    "method_name": "ft_transfer_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |


## 12. Repay from Supplied

- **Test Interface URL**: [https://test-api.burrow.finance/repay_from_supplied](https://test-api.burrow.finance/repay_from_supplied)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Repayment amount, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "actions": [
        {
          "Repay": {
            "max_amount": "1000000000000",
            "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1"
          }
        }
      ]
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "execute"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |

---

## 13. Increase Collateral

- **Test Interface URL**: [https://test-api.burrow.finance/increase_collateral](https://test-api.burrow.finance/increase_collateral)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                |
| ---------- | ---------- | ------------------------------------------ |
| token_id   | String     | Token to operate on                        |
| amount     | String     | Amount to increase collateral, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1",
  "amount": "1000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "actions": [
        {
          "IncreaseCollateral": {
            "max_amount": "1000000000000",
            "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1"
          }
        }
      ]
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "execute"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |


## 14. Decrease Collateral

- **Test Interface URL**: [https://test-api.burrow.finance/decrease_collateral](https://test-api.burrow.finance/decrease_collateral)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                 |
| ---------- | ---------- | ------------------------------------------- |
| token_id   | String     | Token to operate on                         |
| amount     | String     | Amount to decrease collateral, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1",
  "amount": "1000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "msg": "{\"Execute\": {\"actions\": [{\"DecreaseCollateral\": {\"token_id\": \"17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1\", \"max_amount\": \"1000000000000\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "priceoracle.near",
    "method_name": "oracle_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |

## 15. Account Stake Booster

- **Test Interface URL**: [https://test-api.burrow.finance/account_stake_booster](https://test-api.burrow.finance/account_stake_booster)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                         |
| ---------- | ---------- |-------------------------------------|
| duration   | String     | duration                            |
| amount     | String     | Amount to Stake, precision as per metadata |

**Sample Call**:

```
{
  "duration": "1",
  "amount": "1000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "args": {
      "amount": "1000000",
      "duration": 1,
      "receiver_id": "contract.1689937928.burrow.testnet"
    },
    "contract_id": "contract.1689937928.burrow.testnet",
    "method_name": "account_stake_booster"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Stake call parameters                       |

## 16. Account Unstake Booster

- **Test Interface URL**: [https://test-api.burrow.finance/account_unstake_booster](https://test-api.burrow.finance/account_unstake_booster)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                  |
| ---------- | ---------- |----------------------------------------------|

**Sample Call**:

```
No parameters required
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "args": {
      "receiver_id": "contract.1689937928.burrow.testnet"
    },
    "contract_id": "contract.1689937928.burrow.testnet",
    "method_name": "account_unstake_booster"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Unstake call parameters                       |

## 17. Account Farm Claim All

- **Test Interface URL**: [https://test-api.burrow.finance/account_farm_claim_all](https://test-api.burrow.finance/account_farm_claim_all)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                  |
| ---------- | ---------- |----------------------------------------------|

**Sample Call**:

```
No parameters required
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "args": null,
    "contract_id": "contract.1689937928.burrow.testnet",
    "method_name": "account_farm_claim_all"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Claim all call parameters                                     |

## 18. Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/health_factor/juaner1.testnet](https://test-api.burrow.finance/health_factor/juaner1.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.53",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Health level                                                  |

## 19. Max Supply Balance

- **Test Interface URL**: [https://test-api.burrow.finance/max_supply_balance/juaner1.testnet/usdc.fakes.testnet](https://test-api.burrow.finance/max_supply_balance/juaner1.testnet/usdc.fakes.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": "697.280525000000",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
| ---------- |------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Max supply balance                                            |

## 20. Max Burrow Balance

- **Test Interface URL**: [https://test-api.burrow.finance/max_burrow_balance/juaner1.testnet/usdc.fakes.testnet](https://test-api.burrow.finance/max_burrow_balance/juaner1.testnet/usdc.fakes.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": 754.6169796403285,
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
| ---------- |------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Max burrow balance                                            |

## 21. Max Withdraw Balance

- **Test Interface URL**: [https://test-api.burrow.finance/max_withdraw_balance/juaner1.testnet/token.1689937928.burrow.testnet](https://test-api.burrow.finance/max_withdraw_balance/juaner1.testnet/token.1689937928.burrow.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": 4.05951705101648,
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
| ---------- |------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Max withdraw balance                                          |

## 22. Max Adjust Balance

- **Test Interface URL**: [https://test-api.burrow.finance/max_adjust_balance/juaner1.testnet/ref.fakes.testnet](https://test-api.burrow.finance/max_adjust_balance/juaner1.testnet/ref.fakes.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": 5033.559727568972,
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
| ---------- |------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Max adjust balance                                            |

## 22. Max Repay From Wallet Balance

- **Test Interface URL**: [https://test-api.burrow.finance/max_repay_from_wallet/juaner1.testnet/wrap.testnet](https://test-api.burrow.finance/max_repay_from_wallet/juaner1.testnet/wrap.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": 79.38022963223223,
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
| ---------- |------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Max repay from wallet balance                                 |

## 23. Max Repay From Account Balance

- **Test Interface URL**: [https://test-api.burrow.finance/max_repay_from_account/juaner.testnet/ref.fakes.testnet](https://test-api.burrow.finance/max_repay_from_account/juaner.testnet/ref.fakes.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": 79.38022963223223,
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
| ---------- |------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Max repay from account balance                                |

## 24. Account APY

- **Test Interface URL**: [https://test-api.burrow.finance/account_apy/juaner1.testnet/usdc.fakes.testnet](https://test-api.burrow.finance/account_apy/juaner1.testnet/usdc.fakes.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "borrowed_apy": {
      "base_apy": 212.49,
      "total_apy": "212.00",
      "your_apy_data": [
        {
          "token": "ref.fakes.testnet",
          "your_apy": "-0.16"
        },
        {
          "token": "token.1689937928.burrow.testnet",
          "your_apy": "-0.33"
        }
      ]
    },
    "supplied_apy": {
      "base_apy": 162.69,
      "total_apy": "163.45",
      "your_apy_data": [
        {
          "token": "token.1689937928.burrow.testnet",
          "your_apy": "0.72"
        },
        {
          "token": "ref.fakes.testnet",
          "your_apy": "0.04"
        }
      ]
    }
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                     |
|------------|------------|-----------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                    |
| msg        | String     | 'success' for successful return, error message for exceptions   |
| data       | Object     | Account APY data                                                |

## 25. Supply Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/supply_health_factor](https://test-api.burrow.finance/supply_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                                 |
|---------------|------------|-------------------------------------------------------------|
| token_id      | String     | Token to operate on                                         |
| amount        | String     | Amount to Supply, precision as per metadata                 |
| account_id    | String     | Account to health factor, precision as per metadata         |
| is_collateral | Boole      | Whether it is used as collateral, precision as per metadata |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "15000000000000000000000",
	"account_id":"juaner1.testnet",
	"is_collateral":true
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "139.36",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Supply health factor balance                                  |

## 26. Burrow Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/burrow_health_factor](https://test-api.burrow.finance/burrow_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                                 |
|---------------|------------|-------------------------------------------------------------|
| token_id      | String     | Token to operate on                                         |
| amount        | String     | Amount to Burrow, precision as per metadata                 |
| account_id    | String     | Account to health factor, precision as per metadata         |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "10000000000000000000",
	"account_id":"juaner1.testnet"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.53",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Burrow health factor balance                                  |

## 27. Increase Collateral Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/increase_collateral_health_factor](https://test-api.burrow.finance/increase_collateral_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                              |
|---------------|------------|----------------------------------------------------------|
| token_id      | String     | Token to operate on                                      |
| amount        | String     | Amount to Increase collateral, precision as per metadata |
| account_id    | String     | Account to health factor, precision as per metadata      |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "10000000000000000000",
	"account_id":"juaner1.testnet"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.53",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Increase collateral health factor balance                     |

## 28. Decrease Collateral Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/decrease_collateral_health_factor](https://test-api.burrow.finance/decrease_collateral_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                              |
|---------------|------------|----------------------------------------------------------|
| token_id      | String     | Token to operate on                                      |
| amount        | String     | Amount to Decrease collateral, precision as per metadata |
| account_id    | String     | Account to health factor, precision as per metadata      |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "10000000000000000000",
	"account_id":"juaner1.testnet"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.52",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Decrease collateral health factor balance                     |

## 29. Withdraw Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/withdraw_health_factor](https://test-api.burrow.finance/withdraw_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                         |
|---------------|------------|-----------------------------------------------------|
| token_id      | String     | Token to operate on                                 |
| amount        | String     | Amount to Withdraw, precision as per metadata       |
| account_id    | String     | Account to health factor, precision as per metadata |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "100000000000000000000",
	"account_id":"juaner1.testnet"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.46",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Withdraw health factor balance                                |

## 30. Repay From Wallet Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/repay_from_wallet_health_factor](https://test-api.burrow.finance/repay_from_wallet_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                            |
|---------------|------------|--------------------------------------------------------|
| token_id      | String     | Token to operate on                                    |
| amount        | String     | Amount to Repay from wallet, precision as per metadata |
| account_id    | String     | Account to health factor, precision as per metadata    |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "100000000000000000000",
	"account_id":"juaner1.testnet"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.30",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Repay from wallet health factor balance                       |

## 31. Repay From Account Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/repay_from_account_health_factor](https://test-api.burrow.finance/repay_from_account_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                             |
|---------------|------------|---------------------------------------------------------|
| token_id      | String     | Token to operate on                                     |
| amount        | String     | Amount to Repay from account, precision as per metadata |
| account_id    | String     | Account to health factor, precision as per metadata     |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "100000000000000000000",
	"account_id":"juaner1.testnet"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.46",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Repay from account health factor balance                      |

## 31. Repay From Account Health Factor

- **Test Interface URL**: [https://test-api.burrow.finance/repay_from_account_health_factor](https://test-api.burrow.finance/repay_from_account_health_factor)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                                             |
|---------------|------------|---------------------------------------------------------|
| token_id      | String     | Token to operate on                                     |
| amount        | String     | Amount to Repay from account, precision as per metadata |
| account_id    | String     | Account to health factor, precision as per metadata     |

**Sample Call**:

```
{
	"token_id": "ref.fakes.testnet",
	"amount": "100000000000000000000",
	"account_id":"juaner1.testnet"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": "123.46",
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | String     | Repay from account health factor balance                      |

## 32. Check Claim Rewards

- **Test Interface URL**: [https://test-api.burrow.finance/check_claim_rewards/juaner1.testnet](https://test-api.burrow.finance/check_claim_rewards/juaner1.testnet)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": true,
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| code       | String     | Response code, 0 for success                                  |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Boole      | True(Prompt needed), False(Not Prompt needed)                 |

