import near_api
from nacl import signing
from burrow.near_account import NearAccount
from config import GlobalConfig
global_config = GlobalConfig()


def get_viewer_account(account_id) -> NearAccount:
    near_provider = near_api.providers.JsonProvider(global_config.rpc_url)
    key_pair = near_api.signer.KeyPair(signing.SigningKey.generate().__bytes__())
    signer = near_api.signer.Signer(account_id, key_pair)
    return NearAccount(near_provider, signer)


def get_signer_account(account_id) -> NearAccount:
    private_key = global_config.private_key
    near_provider = near_api.providers.JsonProvider(global_config.rpc_url)
    key_pair = near_api.signer.KeyPair(private_key)
    signer = near_api.signer.Signer(account_id, key_pair)
    return NearAccount(near_provider, signer)


if __name__ == "__main__":
    print("############START###########")
    get_signer_account = get_signer_account("juaner.near")
    print("get_signer_account:", get_signer_account)

    get_viewer_account = get_viewer_account("juaner.near")
    print("get_viewer_account:", get_viewer_account)
