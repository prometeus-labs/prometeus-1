from django.db import models
from django.conf import settings


class BlockChainAccount(models.Model):
    address = models.CharField(max_length=120)
    identity = models.CharField(max_length=1024, blank = True, null=True)
    private_key = models.CharField(max_length=1024, blank = True, null=True)
    balance = models.FloatField(blank = True, null=True)

    def __str__(self):
        return self.address

class DataOwner(models.Model):
    blockchain_account = models.ForeignKey(BlockChainAccount, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    storage = models.CharField(max_length=250, blank = True, null=True)
    storage_md5 = models.CharField(max_length=250, blank = True, null=True)

    def __str__(self):
        return self.blockchain_account.address
    
    
class DataValidator(models.Model):
    blockchain_account = models.ForeignKey(BlockChainAccount, on_delete=models.CASCADE)
    system_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_owner = models.ManyToManyField(DataOwner)

    def __str__(self):
        return self.blockchain_account.address
        

class DataMart(models.Model):
    blockchain_account = models.ForeignKey(BlockChainAccount, on_delete=models.CASCADE)
    system_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.blockchain_account.address


class Transaction(models.Model):
    sender =  models.ForeignKey(BlockChainAccount, on_delete=models.CASCADE, related_name='sender', null=True )
    receiver = models.ForeignKey(BlockChainAccount, on_delete=models.CASCADE, related_name='receiver', null=True)
    volume =  models.FloatField(blank = True, null=True) 

    def __str__(self):
        return f"{self.sender.address}_{self.volume}_{self.receiver.address}"
    













