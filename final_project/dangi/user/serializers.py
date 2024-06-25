from rest_framework import serializers
from .models import User, ActivityLevel, DietPeriod
import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password


class UserSignupSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)
    user_birth = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', input_formats=['%Y-%m-%d %H:%M:%S'])

    class Meta:
        model = User
        fields = ['user_id', 'user_nickname', 'password', 'password_check', 'user_birth', 'user_gender', 'activity_level_seq']

    def validate_user_id(self, value):
        if not value:
            raise serializers.ValidationError('사용자 ID를 입력하세요.')
        if not re.match('^[a-zA-Z0-9]{4,12}$', value):
            raise serializers.ValidationError('사용자 ID는 영어와 숫자만 가능하며, 4-12자여야 합니다.')
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError('비밀번호를 입력하세요.')
        if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$', value):
            raise serializers.ValidationError('비밀번호는 영어, 숫자, 특수문자를 최소 1개씩 포함하며, 8-15자여야 합니다.')
        return value

    def validate_password_check(self, value):
        if not value:
            raise serializers.ValidationError('비밀번호 확인을 입력하세요.')
        return value

    def validate_user_nickname(self, value):
        if not value:
            raise serializers.ValidationError('닉네임을 입력하세요.')
        if not re.match('^[a-zA-Z0-9가-힣]{2,15}$', value):
            raise serializers.ValidationError('닉네임은 영어, 숫자, 한글만 가능하며, 2-15자여야 합니다.')
        return value

    def validate_user_birth(self, value):
        if not value:
            raise serializers.ValidationError('생년월일을 입력하세요.')
        return value

    def validate_user_gender(self, value):
        if not value:
            raise serializers.ValidationError('성별을 입력하세요.')
        if value not in ['M', 'F']:
            raise serializers.ValidationError('성별은 "M" 또는 "F"여야 합니다.')
        return value

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({'password_check': '비밀번호 확인이 일치하지 않습니다.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_check')

        # 기본값을 설정할 ActivityLevel 인스턴스 가져오기
        if 'activity_level_seq' not in validated_data or validated_data['activity_level_seq'] is None:
            validated_data['activity_level_seq'] = ActivityLevel.objects.get(pk=1)

        user = User.objects.create(
            user_id=validated_data['user_id'],
            user_nickname=validated_data['user_nickname'],
            user_birth=validated_data['user_birth'],
            user_gender=validated_data['user_gender'],
            activity_level_seq=validated_data['activity_level_seq']
        )
        user.set_password(validated_data['password'])
        user.save()

        # DietPeriod 생성
        DietPeriod.objects.create(
            user_seq=user,
            goal_dt=datetime.now(),  # goal_dt를 실제 목표 날짜로 변경해야 함
            height=user.height,
            weight=user.weight,
            goal_weight=0  # 실제 목표 체중으로 변경해야 함
        )

        return user

class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')

        if not user_id or not password:
            raise serializers.ValidationError("id와 비밀번호 모두 입력해주세요")

        user = authenticate(request=self.context.get('request'), user_id=user_id, password=password)

        if not user:
            raise serializers.ValidationError("회원정보가 일치하지 않습니다")

        refresh = RefreshToken.for_user(user)
        return {
            'user_id': user.user_id,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserHeightDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_nickname', 'height']

#회원정보 조회
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_nickname', 'user_gender', 'user_birth', 'height', 'weight', 'activity_level_seq', 'user_seq']

#회원정보 수정[닉네임만]
class UserUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    current_password_check = serializers.CharField(write_only=True)
    new_nickname = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user
        if not check_password(data['current_password'], user.password):
            raise serializers.ValidationError({'current_password': '현재 비밀번호가 일치하지 않습니다.'})
        if data['current_password'] != data['current_password_check']:
            raise serializers.ValidationError({'current_password_check': '현재 비밀번호 확인이 일치하지 않습니다.'})
        return data

    def update(self, instance, validated_data):
        instance.user_nickname = validated_data['new_nickname']
        instance.save()
        return instance

# diet/serializers.py

class DietPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPeriod
        fields = '__all__'


class UserDietPeriodUpdateSerializer(serializers.Serializer):
    user_seq = serializers.IntegerField()
    height = serializers.FloatField(required=False)
    weight = serializers.FloatField(required=False)
    goal_weight = serializers.FloatField(required=False)
    activity_level_seq = serializers.IntegerField(required=False)
    start_dt = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S', input_formats=['%Y-%m-%d %H:%M:%S'])
    goal_dt = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S', input_formats=['%Y-%m-%d %H:%M:%S'])

    def calculate_bmr(self, weight, height, age, gender):
        if gender == 'M':
            return round(66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age))
        elif gender == 'F':
            return round(655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age))
        return 0

    def calculate_tdee(self, bmr, level_weight):
        return round(bmr * level_weight)

    def update(self, user, validated_data):
        # Get current DietPeriod or create a new one if it does not exist
        try:
            diet_period = DietPeriod.objects.filter(user_seq=user).latest('start_dt')
        except DietPeriod.DoesNotExist:
            diet_period = DietPeriod(user_seq=user)

        # Update user and diet_period fields with validated_data or keep existing values
        user.height = validated_data.get('height', user.height)
        user.weight = validated_data.get('weight', user.weight)
        user.activity_level_seq_id = validated_data.get('activity_level_seq', user.activity_level_seq_id)
        user.save()

        diet_period.height = validated_data.get('height', diet_period.height)
        diet_period.weight = validated_data.get('weight', diet_period.weight)
        diet_period.goal_weight = validated_data.get('goal_weight', diet_period.goal_weight)

        start_dt = validated_data.get('start_dt', diet_period.start_dt)
        goal_dt = validated_data.get('goal_dt', diet_period.goal_dt)
        diet_period.start_dt = start_dt
        diet_period.goal_dt = goal_dt

        # Calculate BMR and TDEE
        birth_date = user.user_birth.date()
        age = (datetime.now().date() - birth_date).days // 365
        bmr = self.calculate_bmr(diet_period.weight, diet_period.height, age, user.user_gender)
        level_weight = ActivityLevel.objects.get(activity_level_seq=user.activity_level_seq_id).level_weight
        tdee = self.calculate_tdee(bmr, level_weight)

        # Calculate period
        period = (goal_dt - start_dt).days

        # Calculate total and daily kcal
        total_kcal = (diet_period.weight - diet_period.goal_weight) * 7700
        daily_kcal = total_kcal / period if period > 0 else 0
        daily_carbo = (daily_kcal * 0.5) / 4
        daily_protein = (daily_kcal * 0.3) / 4
        daily_prov = (daily_kcal * 0.2) / 9

        diet_period.bmr = bmr
        diet_period.tdee = tdee
        diet_period.period = period
        diet_period.total_kcal = total_kcal
        diet_period.daily_kcal = daily_kcal
        diet_period.daily_carbo = daily_carbo
        diet_period.daily_protein = daily_protein
        diet_period.daily_prov = daily_prov
        diet_period.save()

        return user, diet_period