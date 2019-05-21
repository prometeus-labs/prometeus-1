import json, time
from web3 import Web3, HTTPProvider, IPCProvider

accounts = []

my_provider = IPCProvider("../node/chaindata/geth.ipc")
web3 = Web3(my_provider)

web3.eth.defaultAccount = web3.eth.accounts[0]


accounts.append(web3.eth.defaultAccount)
accounts.append(web3.personal.newAccount(""))

web3.personal.unlockAccount(accounts[0], "", 30000)
web3.personal.unlockAccount(accounts[1], "", 30000)

trig = True
while True:
    if trig:
        tx = web3.eth.sendTransaction({'from':accounts[0], 'to':accounts[1], 'value': web3.toWei(1, "ether"), 'gas':21000})
        trig = False
    else:
        tx = web3.eth.sendTransaction({'from':accounts[0], 'to':accounts[1], 'value': web3.toWei(1, "ether"), 'gas':21000})
        trig = True
    
    print(tx)
    
    
    time.sleep(1)




