from web3 import Web3
from libs.ethBIP44.ethLib import HDPrivateKey, HDKey


class EthConnection:
    def __init__(self, provider, mnemonic):
        print("selected provider is {}".format(provider))

        assert len(provider) > 0

        if "http" in provider.lower():
            self.w3 = Web3(Web3.HTTPProvider(provider))
        else:
            self.w3 = Web3(Web3.WebsocketProvider(provider))

        print("connected to {}: {}".format(provider, self.w3.isConnected()))

        if len(mnemonic):
            try:
                self.accounts = []
                self.private_keys = []
                master_key = HDPrivateKey.master_key_from_mnemonic(mnemonic)
                root_keys = HDKey.from_path(master_key, "m/44'/60'/0'/0")
                acct_priv_key = root_keys[-1]
                for i in range(0, 10):
                    keys = HDKey.from_path(acct_priv_key, str(i))
                    priv_key = keys[-1]
                    pub_key = priv_key.public_key
                    address = pub_key.address()
                    self.accounts.append(self.w3.toChecksumAddress(address))
                    self.private_keys.append("0x" + priv_key._key.to_hex())
            except Exception:
                self.accounts = []

    def get_web3(self):
        return self.w3

    def get_accounts(self):
        if len(self.accounts):
            return self.accounts
        return self.w3.eth.accounts

    def signAndSendTransaction(self, address, raw_transaction):
        assert address in self.get_accounts()
        private_key = self.private_keys[self.get_accounts().index(address)]
        signed_transaction = self.w3.eth.account.signTransaction(raw_transaction, private_key)
        return self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
