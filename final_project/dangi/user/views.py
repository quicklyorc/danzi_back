from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserLoginSerializer, UserHeightDetailSerializer, UserProfileSerializer, UserUpdateSerializer
from .models import User, DietPeriod
from rest_framework.permissions import IsAuthenticated
from .serializers import DietPeriodSerializer,UserDietPeriodUpdateSerializer

class UserMemberView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        elif self.request.method in ['GET', 'PUT']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # 회원가입
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.user_id,
                'user_nickname': user.user_nickname,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원정보 조회
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 닉네임 업데이트
    def put(self, request):
        serializer = UserUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.update(request.user, serializer.validated_data)
            return Response({
                "user_id": user.user_id,
                "user_nickname": user.user_nickname
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#아이디 중복 체크
class CheckUserId(APIView):
    permission_classes = [AllowAny]  # 인증 없이 접근 가능하도록 설정
    def get(self, request, user_id):
        if User.objects.filter(user_id=user_id).exists():
            return Response({"message": "사용자 ID가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "사용자 ID를 사용할 수 있습니다."}, status=status.HTTP_200_OK)

#로그인
class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#다이어트 정보 입력 확인 [height값 체크]
class UserHeight(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserHeightDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 클라이언트 측에서 토큰을 삭제하기 위한 로그아웃 엔드포인트
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserDeactivate(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.del_yn = 'Y'
        user.save()
        return Response({"detail": "회원탈퇴가 성공적으로 완료되었습니다."}, status=status.HTTP_200_OK)


class DietPeriodView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        diet_period = DietPeriod.objects.filter(user_seq=user)
        if not diet_period.exists():
            return Response({"detail": "다이어트 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DietPeriodSerializer(diet_period, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserDietPeriodUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user, diet_period = serializer.update(user, serializer.validated_data)
            return Response({
                "user_id": user.user_id,
                "height": user.height,
                "weight": user.weight,
                "goal_weight": diet_period.goal_weight,
                "activity_level_seq": user.activity_level_seq_id,
                "bmr": diet_period.bmr,
                "tdee": diet_period.tdee,
                "period": diet_period.period,
                "total_kcal": diet_period.total_kcal,
                "daily_kcal": diet_period.daily_kcal,
                "daily_carbo": diet_period.daily_carbo,
                "daily_protein": diet_period.daily_protein,
                "daily_prov": diet_period.daily_prov
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DietRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            diet_period = DietPeriod.objects.filter(user_seq=user).latest('start_dt')
        except DietPeriod.DoesNotExist:
            return Response({"detail": "다이어트 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        total_kcal = diet_period.total_kcal
        if total_kcal is None or total_kcal == 0:
            return Response({"detail": "총 칼로리 정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        recommended_period = int(total_kcal / 500)
        return Response({"recommended_period": recommended_period}, status=status.HTTP_200_OK)