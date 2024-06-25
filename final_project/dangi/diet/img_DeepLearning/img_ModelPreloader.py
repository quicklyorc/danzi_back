import boto3
import os
import cv2
import numpy as np
from django.conf import settings
from botocore.client import Config
from tensorflow.keras.models import load_model

s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='ap-northeast-2',  # 실제 사용하는 AWS S3 버킷의 리전
        config=Config(signature_version='s3v4')  # 인증 메커니즘 설정
    )

bucket_name = settings.AWS_STORAGE_BUCKET_NAME

#s3 경로
s3_weights_file = 'yolo/yolov3_training_final.weights'
s3_cfg_file = 'yolo/yolov3_testing.cfg'
s3_name_file = 'yolo/obj.names'

s3_quantity_file = 'keras/model_0.86_0.40_saved.h5'
s3_classify_file = 'keras/SGD_checkpoint_10.h5'

# 로컬에 저장할 파일 이름
weights_file = 'diet/models/yolo/yolov3_training_final.weights'
cfg_file = 'diet/models/yolo/yolov3_testing.cfg'
name_file = 'diet/models/yolo/obj.names'

quantity_local = 'diet/models/keras/SGD_checkpoint_10.h5'
classify_local = 'diet/models/keras/model_0.86_0.40_saved.h5'


if not os.path.exists(weights_file):
    os.makedirs('diet/models/yolo', exist_ok=True)
    # 파일 다운로드
    s3_client.download_file(bucket_name, s3_weights_file, weights_file)
    s3_client.download_file(bucket_name, s3_cfg_file, cfg_file)
    s3_client.download_file(bucket_name, s3_name_file, name_file)

if not os.path.exists(quantity_local):
    os.makedirs('diet/models/keras', exist_ok=True)
    s3_client.download_file(bucket_name, s3_quantity_file, quantity_local)
    
if not os.path.exists(classify_local):
    os.makedirs('diet/models/keras', exist_ok=True)
    s3_client.download_file(bucket_name, s3_classify_file, classify_local)
    
object_yolonet = cv2.dnn.readNet(cfg_file, weights_file)
object_yolonet.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) # OpenCV의 기본 백엔드를 사용하도록 설정
object_yolonet.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # CPU 설정 # or DNN_TARGET_OPENCL, DNN_TARGET_CUDA


quantity_model = load_model(quantity_local)
classify_model = load_model(classify_local)
