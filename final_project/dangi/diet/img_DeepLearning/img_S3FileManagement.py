import boto3
import uuid
from django.conf import settings
from botocore.client import Config

class S3ImgUploader:
    def __init__(self, file):
        self.file = file
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        )

    def upload(self):
    
        url = 'foodimg'+'/'+uuid.uuid1().hex
        
        self.s3_client.upload_fileobj(
            self.file, 
            settings.AWS_STORAGE_BUCKET_NAME,
            url,
            ExtraArgs={
                "ContentType": self.file.content_type
            }
        )
        return url
    
    def delete(self, img_key):
        # S3 객체 삭제
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        self.s3_client.delete_object(Bucket=bucket_name, Key=img_key)

        print(f'{img_key} deleted')
        
    
  
    
class S3ImgurlMapper:
    def __init__(self, url):
        self.url = url

        # AWS S3 클라이언트 설정

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name='ap-northeast-2',  # 실제 사용하는 AWS S3 버킷의 리전
            config=Config(signature_version='s3v4')  # 인증 메커니즘 설정
        )

    def getImage(self):
        
        # S3 버킷 및 이미지 키
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        image_key = self.url  #  S3에서 이미지의 키 (파일 경로)
        
        try:
            # S3에서 이미지 파일 가져오기
            s3_response = self.s3_client.get_object(Bucket=bucket_name, Key=image_key)
            image_data = s3_response['Body'].read()

            return image_data
        except Exception as e:
            return str(e)
        
    def urlmap(self):

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        region_name = 'ap-northeast-2'
        image_key = self.url  # S3에서 이미지의 키 (파일 경로)
        mapped_url = f'https://{bucket_name}.s3.{region_name}.amazonaws.com/{image_key}'
        # 클라이언트에게 이미지 URL 전송
        return mapped_url