"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import UserMemberView, CheckUserId, UserLogin, UserHeight, UserLogout, UserDeactivate, DietPeriodView, DietRecommendationView
from diet.views import DietMealsView, ImageInfo


urlpatterns = [
    path('admin/', admin.site.urls), # 이걸로 들어가야 내용 확인 가능
    # path('api-auth/', include('rest_framework.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # User URLS
    path('user/member/', UserMemberView.as_view(), name='user_member'),  # 회원가입 및 사용자 정보 조회
    path('user/member/<str:user_id>/', CheckUserId.as_view(), name='check_user_id'), #아이디 중복 체크
    path('user/login/', UserLogin.as_view(), name='user_login'), #로그인
    path('user/logout/', UserLogout.as_view(), name='user_logout'),  # 로그아웃
    path('user/delete/', UserDeactivate.as_view(), name='user_delete'),  # 회원탈퇴
    path('user/diet_height/', UserHeight.as_view(), name='user_detail'),  # 다이어트 정보 입력 확인 [height 값 체크]
    path('user/diet_info/', DietPeriodView.as_view(), name='diet_period'),  # 다이어트 기간 정보 조회 및 업데이트
    path('user/diet_info/recommend_period/', DietRecommendationView.as_view(), name='diet_recommendation'),  # 다이어트 추천 기간 조회

    #Diet URLS
    path('diet/meals/', DietMealsView.as_view(), name='diet_record'),
    path('diet/meals/<int:pk>/', DietMealsView.as_view(), name='diet_meals_update'),
    path('diet/record/image', ImageInfo.as_view(), name='image_info'),

]
