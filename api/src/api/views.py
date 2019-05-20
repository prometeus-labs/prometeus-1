
import time
import datetime
import pytz

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Max
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status, permissions, views
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet, ViewSet


from .serializers import (DataVAlidatorSerializer)
from .models import (DataVAlidator, BlockChainAccount)

from prometeus.settings import web3_
import sys
sys.path.insert(0,'../../../')
import validator.utils
import core.utils

node = '../../node/chaindata/keystore'
    
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
