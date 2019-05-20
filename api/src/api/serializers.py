from rest_framework import serializers
from .models import (DataVAlidator)

class DataVAlidatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataVAlidator
        fields = '__all__'