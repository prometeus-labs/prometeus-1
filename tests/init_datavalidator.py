import sys
sys.path.insert(0, '../lib/')

from web3 import Web3, HTTPProvider, IPCProvider
import validator, core, time
from core.utils import eth_create_new_account

my_provider = IPCProvider("../node/chaindata/geth.ipc")
web3 = Web3(my_provider)

default_account = web3.eth.accounts[0]
web3.personal.unlockAccount(default_account, "", 30000)


eth_account = core.utils.eth_create_new_account(web3, '../node/chaindata/keystore')
eth_account_check_summ = web3.toChecksumAddress(eth_account["account"])

tx = web3.eth.sendTransaction({'from':default_account, 'to':eth_account_check_summ, 'value': web3.toWei(1, "ether"), 'gas':21000})

time.sleep(2) #while for node done transaction



eth_account['balance'] = web3.eth.getBalance( eth_account_check_summ )

ret = {
    'blockchain_account': eth_account,
    'system_account': {'login':'login', 'password': 'password'}
}

print(ret)