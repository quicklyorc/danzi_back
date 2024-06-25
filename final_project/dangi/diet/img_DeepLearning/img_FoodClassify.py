import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from .img_ModelPreloader import classify_model

class FoodClassifier:
    def __init__(self, dict):
        self.images_dict = dict
        self.foodnames = ()

    def menupredict(self):

        # 이미지 전처리
        img = self.images_dict['dish']
        img = img_to_array(img)
        img = tf.keras.applications.mobilenet_v3.preprocess_input(img)

        img_size=(224,224)

        input_img = cv2.resize(img, img_size)
        input_img = np.expand_dims(input_img, axis=0)

        bestmodel = classify_model

        # 모델 예측
        y_pred_prob = bestmodel.predict(input_img)
        y_pred = np.argmax(y_pred_prob[0])

        # foodmenu = self.foodnames[y_pred] !!!임시!!추후수정!!!!
        foodmenu = int(y_pred)
        return foodmenu