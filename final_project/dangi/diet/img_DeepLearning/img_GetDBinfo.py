# 식품영양 DB에서 음식명 읽어옴

class FoodInfoChecker:
    def __init__(self, foodmenu, quantity_level):
        self.foodmenu = foodmenu
        self.quantity_level = quantity_level

    def get_nutrition_info(self):
        # foodmenu와 일치하는 행 가져옴
        # 각 feature들 가져오기

        # db연동 전 임시 값들.
        quantity = 375
        kcal = 300
        carbo = 23.5
        protein = 21.2
        prov = 11.5

        return quantity, kcal, carbo, protein, prov