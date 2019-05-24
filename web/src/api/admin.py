from django.contrib import admin

# Register your models here.
from .models import DataVAlidator, BlockChainAccount

class DataVAlidatorAdmin(admin.ModelAdmin):
    pass
admin.site.register(DataVAlidator, DataVAlidatorAdmin)