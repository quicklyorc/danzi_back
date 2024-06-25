# diet/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Diet, DailyDiet
from .serializers import DietSerializer
from user.models import User
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime
from django.http import JsonResponse
from diet.img_DeepLearning import img_S3FileManagement, img_Inference

class DietMealsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user  # 토큰 인증을 통해 얻은 사용자
        user_seq = user.user_seq

        data = request.data
        date_str = data.get('date')
        date_obj = parse_datetime(date_str)

        if not date_obj:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # 동일한 user_seq 번호를 갖는 daily_diet 찾기 또는 생성
        daily_diet, created = DailyDiet.objects.get_or_create(
            user_seq=user,
            date__date=date_obj.date(),
            defaults={
                'kcal': data.get('kcal'),
                'carbo': data.get('carbo'),
                'protein': data.get('protein'),
                'prov': data.get('prov'),
                'date': date_obj,
            }
        )

        if not created:
            # 동일한 날짜에 대한 daily_diet이 이미 존재하면 업데이트
            daily_diet.kcal += data.get('kcal', 0)
            daily_diet.carbo += data.get('carbo', 0)
            daily_diet.protein += data.get('protein', 0)
            daily_diet.prov += data.get('prov', 0)
            daily_diet.save()

        # Diet 레코드 생성
        diet_data = {
            'daily_diet_seq': daily_diet.daily_diet_seq,
            'user_seq': user_seq,
            'name': data.get('name'),
            'quantity': data.get('quantity'),
            'kcal': data.get('kcal'),
            'carbo': data.get('carbo'),
            'protein': data.get('protein'),
            'prov': data.get('prov'),
            'date': date_obj,
            'food_img': data.get('food_img', None),
        }

        serializer = DietSerializer(data=diet_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            diet = Diet.objects.get(pk=pk)
        except Diet.DoesNotExist:
            return Response({'error': 'Diet not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # 이전 daily_diet의 값을 원래대로 되돌림
        previous_daily_diet = diet.daily_diet_seq

        # 현재 값들을 저장해둠
        original_kcal = diet.kcal
        original_carbo = diet.carbo
        original_protein = diet.protein
        original_prov = diet.prov

        # 저장 전 daily_diet에서 기존 값 빼기
        previous_daily_diet.kcal -= original_kcal
        previous_daily_diet.carbo -= original_carbo
        previous_daily_diet.protein -= original_protein
        previous_daily_diet.prov -= original_prov
        previous_daily_diet.save()

        # diet 값 업데이트
        diet.name = data.get('name', diet.name)
        diet.quantity = data.get('quantity', diet.quantity)
        diet.kcal = data.get('kcal', diet.kcal)
        diet.carbo = data.get('carbo', diet.carbo)
        diet.protein = data.get('protein', diet.protein)
        diet.prov = data.get('prov', diet.prov)
        date_str = data.get('date', diet.date)
        diet.date = parse_datetime(date_str) if date_str != diet.date else diet.date
        diet.food_img = data.get('food_img', diet.food_img)

        # 동일한 user_seq 번호를 갖는 daily_diet 찾기 또는 생성
        daily_diet, created = DailyDiet.objects.get_or_create(
            user_seq=diet.user_seq,
            date__date=diet.date.date(),
            defaults={
                'kcal': diet.kcal,
                'carbo': diet.carbo,
                'protein': diet.protein,
                'prov': diet.prov,
                'date': diet.date,
            }
        )

        if not created:
            # 새로운 daily_diet에 값 추가
            daily_diet.kcal += diet.kcal
            daily_diet.carbo += diet.carbo
            daily_diet.protein += diet.protein
            daily_diet.prov += diet.prov
            daily_diet.save()

        # diet 값 저장
        diet.daily_diet_seq = daily_diet
        diet.save()

        serializer = DietSerializer(diet)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageInfo(APIView):
    # 일단 AllowAny인데 추후 변경 가능
    permission_classes = [AllowAny]
    
    def post(self, reqest):
        
        if "img" not in reqest.FILES:
            return JsonResponse({'error': 'No file provided'}, status=status.HTTP_204_NO_CONTENT)
        
        # S3에 이미지 업로드
        uploader = img_S3FileManagement.S3ImgUploader(file = reqest.FILES["img"])
        imgurl = uploader.upload()

        # url 따오기, 이미지 가져오기
        urlmapper = img_S3FileManagement.S3ImgurlMapper(url=imgurl)
        bytes_img = urlmapper.getImage()
        mapped_url = urlmapper.urlmap()

        # 이미지 추론
        inference = img_Inference.DLInference(bytes_img=bytes_img)
        foodmenu, quantity, kcal, carbo, protein, prov = inference.predict()

        
        # model = Student.objects.get(student_id = student_id)
        # serializer = StudentSerializer(model)
        
        return JsonResponse(
                {
                "food_name": foodmenu,
                "img_url": mapped_url,
                "calories": kcal,
                "weight": quantity,
                "carbohydrate": carbo,
                "protein": protein,
                "fat": prov
                }
            )