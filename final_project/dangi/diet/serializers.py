# diet/serializers.py
from rest_framework import serializers
from .models import Diet

class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'
