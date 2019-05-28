
import time
import hashlib

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework import status, permissions, views

from .models import (DataValidator, BlockChainAccount, DataOwner, DataMart)

from prometeus.settings import web3_, PROMETEUS_LIB_PATH, NODE_PATH, STORAGE_PATH


import sys
sys.path.insert(0, PROMETEUS_LIB_PATH)

import validator.utils
import core.utils

node = NODE_PATH + 'keystore'

class InitDataValidatorView(views.APIView):
    permission_classes = [ permissions.AllowAny]

    def get(self, request, format=None):
        acc_types = ['mart', 'owner', 'validator']
        ret = {}
        user = request.user
        blockchain_account = request.GET.get('blockchain_account')
        account_type = request.GET.get('type')
      
        if blockchain_account:
            pass
        else:
            default_account = web3_.eth.accounts[0]
            web3_.personal.unlockAccount(default_account, "", 30000)
            eth_account = core.utils.eth_create_new_account(web3_, node)
            eth_account_check_summ = web3_.toChecksumAddress(eth_account["account"])
            tx = web3_.eth.sendTransaction({'from':default_account, 'to':eth_account_check_summ, 'value': web3_.toWei(1, "ether"), 'gas':21000})
            time.sleep(2)
            eth_account['balance'] = web3_.eth.getBalance( eth_account_check_summ )

            ret['blockchain_account'] = eth_account
            ret['info'] = 'dev_node: balance granted for demo purposes'


            bca = BlockChainAccount(address=eth_account['account'])
            bca.save()

            if not user.is_authenticated:

                if account_type and account_type in acc_types:
                    user = User.objects.create_user(username=eth_account['account'].split('0x')[1],
                                                    password=eth_account['account'].split('0x')[1])
                    user.save()
                                        
                    if account_type == 'mart':
                        dv = DataMart(blockchain_account=bca, system_account=user)
                        dv.save()
                    elif account_type == 'validator':
                        dv = DataValidator(blockchain_account=bca, system_account=user)
                        dv.save()
                    elif account_type == 'owner':
                        dv = DataOwner(blockchain_account=bca, system_account=user)
                        dv.save()

                    ret['system_account'] = {'login':user.username, 'password':eth_account['account'].split('0x')[1] }
                else:
                    ret = {'info': f"no account type {acc_types} has specified", "error_code":1004}

     
        return JsonResponse(ret)

class InitDataOwner(views.APIView):
    permission_classes = [ permissions.AllowAny]

    def post(self, request, format=None):
        ret = {}
        if 'validator' in request.data.keys() and 'data' in request.data.keys():
            is_valid = core.utils.eth_is_valid_address(web3_, request.data['validator'])

            if is_valid:

                #-----------------------------------------------------------------------
                # Encrypt DataOwner data received from DataValidator request
                #-----------------------------------------------------------------------

                encrypted = validator.utils.encrypt2(str(request.data['data']))
                encrypted_body = encrypted['encrypted']
                encrypted_private_key = encrypted['private_key']

                blockchain_account = core.utils.eth_create_new_account(web3_, node)
                do_acc = BlockChainAccount(address = blockchain_account['account'])
                do_acc.save()

                encrypted_file_name = f"{blockchain_account['account'].split('0x')[1]}_{request.data['validator'].split('0x')[1]}".lower()
                url_encrypted_file = f"http://storage.prometeus.io/{encrypted_file_name}"

                newFile = open(f"{STORAGE_PATH}{encrypted_file_name}", "wb")
                newFile.write(encrypted_body)
                newFile.close()

                ret = {
                        'blockchain_account': str(blockchain_account),
                        'storage_url': str(url_encrypted_file),
                        'validator':  str(request.data['validator']),
                        'private_key': str(encrypted_private_key),
                        'md5': hashlib.md5(encrypted_body).hexdigest()
                    }

                dv = DataValidator.objects.get(blockchain_account__address = request.data['validator'])                
                do = DataOwner(blockchain_account =  do_acc )
                do.save()
                dv.data_owner.add(do)

                print(do.blockchain_account.address)
                
            else:
                ret = {'info': f"not valid blokchain address {request.data['validator']}", 'error_code':1002}

        else:
            ret = {'info': 'not valid params', 'error_code':1001}

        return JsonResponse(ret)


class Scanner(views.APIView):
    permission_classes = [ permissions.AllowAny]
    
    def get(self, request, format=None):
        ret = {}

        user = request.user
        blockchain_address = request.GET.get('blockchain_address')
        

        blockchain_account = BlockChainAccount.objects.filter(address = blockchain_address).first()

        print(blockchain_account)

        if blockchain_account:
            addrss_types = [DataMart, DataValidator, DataOwner]
            for i in addrss_types:
                account = i.objects.filter(blockchain_account = blockchain_account).first()
                if account:
                    account_type = None
                    if type(account) == DataOwner:
                        ret['blockchain_address'] = account.blockchain_account.address
                        ret['type'] = 'data_owner'
                        ret['updated'] = account.updated
                        ret['storage'] = account.storage
                        ret['storage_md5'] = account.storage_md5
                        validator = DataValidator.objects.filter(data_owner=account).first()
                        ret['validator'] = validator.blockchain_account.address
                    
                    elif type(account) == DataValidator:
                        account_type = 'data_validator'
                    elif type(account) == DataMart:
                        account_type = 'data_mart'
        else:
            ret = {'info': 'not a valid address in Prometeus network', 'error_code':1003}

        return JsonResponse(ret)

