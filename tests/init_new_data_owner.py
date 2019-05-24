import sys, uuid, secrets
sys.path.insert(0, '../lib/')

import json, time
import hashlib
from web3 import Web3, HTTPProvider, IPCProvider

from core.utils import eth_create_new_account
import validator


my_provider = IPCProvider("../node/chaindata/geth.ipc")
web3 = Web3(my_provider)


#=========================================================
# DataValidator: send GET request to /init_new_data_owner
# params: {"data": str(),
#          "data_validator": str(eth.account) }
#=========================================================

#------------------------------------------------
# Data Validator forms request and call REST API  
# data - is a structure from API Get request
#------------------------------------------------
data = {"data":"data owner data",
        "data_validator": "0x" + secrets.token_bytes(20).hex()}



#=============================
# System: work on GET request
#=============================

data_validator = data['data_validator']

#-----------------------------------------------------------------------
# Encrypt DataOwner data received from DataValidator request
#-----------------------------------------------------------------------

encrypted = validator.encrypt2(str(data['data']))
encrypted_body = encrypted['encrypted']
encrypted_private_key = encrypted['private_key']

#-----------------------------------------
# Create new account in blockchain
#-----------------------------------------
blockchain_account = eth_create_new_account(web3, '../node/chaindata/keystore')

#--------------------------------data_validator--------------------------------------------
# Save encrypted into storage and genearate link, create record to db
#----------------------------------------------------------------------------
 
encrypted_file_name = f"{blockchain_account['account'].split('0x')[1]}_{data_validator.split('0x')[1]}".lower()
url_encrypted_file = f"http://storage.prometeus.io/{encrypted_file_name}"

# newFile = open(encrypted_file_name, "wb")
# newFile.write(encrypted_body)
# newFile.close()


#--------------------------------------------------------------
# Responds on /init_new_data_owner
# Save to System DB
#--------------------------------------------------------------
ret = {
    'blockchain_account': blockchain_account,
    'storage_url': url_encrypted_file,
    'data_validator':  data_validator,
    'private_key': encrypted_private_key,
    'md5': hashlib.md5(encrypted_body).hexdigest()
}

print(ret)

