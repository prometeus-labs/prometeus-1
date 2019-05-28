from django.contrib import admin

# Register your models here.
from .models import DataValidator, BlockChainAccount, DataOwner, DataMart

class DataVAlidatorAdmin(admin.ModelAdmin):
    pass

class DataOwnerAdmin(admin.ModelAdmin):
    pass

class BlockChainAccountAdmin(admin.ModelAdmin):
    pass

class DataMartAdmin(admin.ModelAdmin):
    pass



admin.site.register(DataValidator, DataVAlidatorAdmin)
admin.site.register(DataOwner, DataOwnerAdmin)
admin.site.register(BlockChainAccount, BlockChainAccountAdmin)
admin.site.register(DataMart, DataMartAdmin)