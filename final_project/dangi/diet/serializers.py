# diet/serializers.py
from rest_framework import serializers
from .models import Diet, Food

class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'
        
    
class FoodInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, unique=True)
    quantity = serializers.IntegerField()
    kcal = serializers.IntegerField()
    carbo = serializers.IntegerField()
    protein = serializers.IntegerField()
    prov = serializers.IntegerField()
    
    class Meta:
        model = Food
        fields = ['name','quantity','kcal','carbo','protein','prov']
