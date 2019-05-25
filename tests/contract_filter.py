import sys, uuid, secrets
sys.path.insert(0, '..')

import json, time
import hashlib
from web3 import Web3, HTTPProvider, IPCProvider

from core.utils import eth_create_new_account
import validator


my_provider = IPCProvider("../node/chaindata/geth.ipc")
web3 = Web3(my_provider)

contract_address = eth_account_check_summ = web3.toChecksumAddress("0xc1d996fac7145df2f270dc5f1f200086c54e6c93")

with open('contract.json', 'r') as abi_definition:
        abi = json.load(abi_definition)['contracts']['../contract/prometeus.sol:Prometeus']['abi']

contract = web3.eth.contract(address = contract_address, abi=abi)

event_filter = contract.eventFilter('Approval', {'fromBlock': 0, 'toBlock': 'latest'})
event_logs = event_filter.get_all_entries()

for i in event_logs:
        print(i)


# contract_fiter = web3.eth.filter({'fromBlock':0,
#                                   'toBlock':'latest',
#                                   "address":contract_address})


# event_log = web3.eth.getFilterLogs(contract_fiter.filter_id)
# print(event_log)


#while True:
        
#        for event in contract_fiter.get_new_entries():
#            print(event)
        #     block_hash = event.hex()
        #     block = web3.eth.getBlock(block_hash, full_transactions=True)
        #     transactions = block['transactions']
        #     for tx in transactions:
        #         #print('From wallet: ', tx['from'])
        #         #print('Value ETH: ', tx['value'])
        #         print(tx)
            
           
            
#        time.sleep(2)

