import numpy as np
import cv2
from .img_ModelPreloader import quantity_model

class FoodQuantityPredictor:
    def __init__(self, dict):
        self.images_dict = dict
        self.quantity_level = (0.25, 0.5, 0.75, 1, 1.25)

    def quantitypredict(self):

        bestmodel = quantity_model

        coin_image = self.images_dict["coin"]

        dish_image = self.images_dict["dish"]

        img_size=(224,224)

        cH, cW = coin_image.shape[:2]
        dH, dW = dish_image.shape[:2]

        # 동전 접시 비율계산
        ratio = round((dH * dW) / (cH * cW), 2)
        np_ratio = np.array([ratio])

        # 이미지 전처리
        input_img = cv2.resize(dish_image, img_size)
        input_img = np.expand_dims(input_img, axis=0)


        # 모델 예측
        y_pred_prob = bestmodel.predict([input_img, np_ratio])

        # 예측결과를 quantity로 변환
        y_pred = np.argmax(y_pred_prob[0])
        quantity_level = self.quantity_level[y_pred]
        return quantity_level