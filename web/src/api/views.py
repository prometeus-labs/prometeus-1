
import time
import hashlib

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework import status, permissions, views

from .models import (DataVAlidator, BlockChainAccount)

from prometeus.settings import web3_

import sys
sys.path.insert(0,'../')

import validator.utils
import core.utils

node = '/node_data/keystore'

class InitDataValidatorView(views.APIView):
    permission_classes = [ permissions.AllowAny]

    def get(self, request, format=None):
        ret = {}
        user = request.user
        blockchain_account = request.GET.get('blockchain_account')

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

                user = User.objects.create_user(username=eth_account['account'].split('0x')[1],
                                                password=eth_account['account'].split('0x')[1])

                dv = DataVAlidator(blockchain_account=bca, system_account=user)
                dv.save()

                ret['system_account'] = {'login':user.username, 'password':eth_account['account'].split('0x')[1] }


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

                encrypted = node.validator.utils.encrypt2(str(request.data['data']))
                encrypted_body = encrypted['encrypted']
                encrypted_private_key = encrypted['private_key']

                blockchain_account = core.utils.eth_create_new_account(web3_, node)
                encrypted_file_name = f"{blockchain_account['account'].split('0x')[1]}_{request.data['validator'].split('0x')[1]}".lower()
                url_encrypted_file = f"http://storage.prometeus.io/{encrypted_file_name}"

                newFile = open(f"/storage/{encrypted_file_name}", "wb")
                newFile.write(encrypted_body)
                newFile.close()

                ret = {
                        'blockchain_account': str(blockchain_account),
                        'storage_url': str(url_encrypted_file),
                        'validator':  str(request.data['validator']),
                        'private_key': str(encrypted_private_key),
                        'md5': hashlib.md5(encrypted_body).hexdigest()
                    }


            else:
                ret = {'info': f"not valid blokchain address {request.data['validator']}", 'error_code':1002}

        else:
            ret = {'info': 'not valid params', 'error_code':1001}

        return JsonResponse(ret)
