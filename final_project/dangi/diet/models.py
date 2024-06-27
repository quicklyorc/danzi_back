# diet/models.py
from django.db import models
from user.models import User  # user 앱의 User 모델을 가져옴

class DailyDiet(models.Model):
    daily_diet_seq = models.AutoField(primary_key=True)
    user_seq = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_seq')
    date = models.DateTimeField()
    kcal = models.IntegerField()
    carbo = models.IntegerField()
    protein = models.IntegerField()
    prov = models.IntegerField()
    success_yn = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'daily_diet'

class Diet(models.Model):
    diet_seq = models.AutoField(primary_key=True)
    daily_diet_seq = models.ForeignKey(DailyDiet, on_delete=models.CASCADE, db_column='daily_diet_seq')
    user_seq = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_seq')
    name = models.CharField(max_length=100)
    quantity = models.FloatField(blank=True, null=True)
    kcal = models.IntegerField()
    carbo = models.IntegerField()
    protein = models.IntegerField()
    prov = models.IntegerField()
    reg_at = models.DateTimeField(auto_now_add=True)
    mod_at = models.DateTimeField(blank=True, null=True)
    food_img = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        db_table = 'diet'
        
class Food(models.Model):
    food_seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    kcal = models.IntegerField()
    carbo = models.IntegerField()
    protein = models.IntegerField()
    prov = models.IntegerField()

    class Meta:
        db_table = 'food'

class FoodAmount(models.Model):
    food_amount_seq = models.AutoField(primary_key=True)
    level = models.CharField(max_length=45, unique=True)
    level_weight = models.FloatField()

    class Meta:
        db_table = 'food_amount'
