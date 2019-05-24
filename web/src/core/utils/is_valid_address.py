
def eth_is_valid_address(web3, blokchanin_address):
    ret = None
    
    blokchanin_address = web3.toChecksumAddress(blokchanin_address)
    
    transaction_count = web3.eth.getTransactionCount(blokchanin_address)
    balance = web3.eth.getBalance(blokchanin_address) 
    
    if balance !=0 or transaction_count != 0:
        ret = {'balance': balance, 'transactions': transaction_count, 'address': blokchanin_address}

    return ret