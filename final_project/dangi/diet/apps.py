from django.apps import AppConfig
import sys
import cv2

from diet.img_DeepLearning import img_ModelPreloader
from diet.img_DeepLearning import img_ObjectDetect
from diet.img_DeepLearning import img_FoodClassify 
from diet.img_DeepLearning import img_FoodQuantity


class DietConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diet'

    def ready(self):
        if 'runserver' in sys.argv:
            img_ModelPreloader.object_yolonet
            img_ModelPreloader.quantity_model
            img_ModelPreloader.classify_model
            
            # 웜업(사전에 1회 모델 추론으로 예열)
            image_file_path = 'diet/models/warmup.JPG'

            # 이미지 파일을 이진 모드로 열기
            image_binary = cv2.imread(image_file_path)
            
            
            print("Warmup Yolo Model...")
            objectdetector = img_ObjectDetect.ObjectDetector(image=image_binary)
            layerOutputs = objectdetector.detect_objects()
            output_dict = objectdetector.crop_image(layerOutputs)
            print("Yolo Model warmup Complete!")

            # 음식 분류
            print("Warmup Classify Model...")
            foodclassifier = img_FoodClassify.FoodClassifier(dict=output_dict)
            foodmenu = foodclassifier.menupredict()
            print("Classify Model warmup Complete!")

            # 음식량 추정
            print("Warmup Quantity Model...")
            quantitypredictor = img_FoodQuantity.FoodQuantityPredictor(dict=output_dict)
            quantity_level = quantitypredictor.quantitypredict()
            print("Quantity Model warmup Complete!")
