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

    def __str__(self):
        return self.blockchain_account.address
    
    
class DataValidator(models.Model):
    blockchain_account = models.ForeignKey(BlockChainAccount, on_delete=models.CASCADE)
    system_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_owner = models.ManyToManyField(DataOwner)

    def __str__(self):
        return self.blockchain_account.address









