import cv2
import numpy as np
from .img_ModelPreloader import object_yolonet, name_file

class ObjectDetector:
    def __init__(self, image):

        self.image = np.array(image)

        # Yolov3 모델 로드
        self.net = object_yolonet
        
        # 클래스 파일 로드
        self.classes = None
        classesFile = name_file
        with open(classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

    # 객체 탐지
    def detect_objects(self):
        # blobFromImage 이미지 전처리
        blob = cv2.dnn.blobFromImage(self.image, 1/255.0, (416,416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.net.getUnconnectedOutLayersNames()) # 탐지된 객체 리스트
        return layerOutputs

    # 바운딩 박스 그리기
    def crop_image(self, layerOutputs, confidence_threshold=0.5, nms_threshold=0.4):
        frameHeight, frameWidth = self.image.shape[:2]
        class_ids = []
        boxes = []
        confidences = []
        output_dict = {}

        for output in layerOutputs:
            for detection in output:
                # 순서대로 x,y,w,h,confidence점수, detection[5:]부터 객체 클래스 확률
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # NMSBoxes : 박스가 겹치면 신뢰도가 가장 높은 상자 하나만 선택
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
        
        if not (2 in class_ids and 3 in class_ids):
            

        # 객체 정보 출력
        for i in indices:
            box = boxes[i]
            left, top, width, height = box
            print(class_ids)
            class_id = class_ids[i]
            # 동전:2 그릇:3
            if class_id in (2,3):
                class_name = self.classes[class_id]
                cropped_image = self.image[top:top + height, left:left + width]
                output_dict[class_name] = cropped_image

        # 반환 값 => {coin:동전크롭이미지, dish:그릇크롭이미지}
        return output_dict
        
    