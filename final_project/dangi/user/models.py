from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class ActivityLevel(models.Model):
    activity_level_seq = models.AutoField(primary_key=True)
    level = models.CharField(max_length=45)
    level_desc = models.CharField(max_length=200)
    level_weight = models.FloatField()

    class Meta:
        db_table = 'activity_level'


class UserManager(BaseUserManager):
    def create_user(self, user_id, user_nickname, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID field must be set')

        # 기본값을 설정할 ActivityLevel 인스턴스 가져오기
        if 'activity_level_seq' not in extra_fields or extra_fields['activity_level_seq'] is None:
            extra_fields['activity_level_seq'] = ActivityLevel.objects.get(pk=1)

        user = self.model(
            user_id=user_id,
            user_nickname=user_nickname,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, user_nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_id, user_nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_seq = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=25, unique=True)
    activity_level_seq = models.ForeignKey(ActivityLevel, on_delete=models.DO_NOTHING, db_column='activity_level_seq',
                                           null=True, blank=True)
    user_nickname = models.CharField(max_length=45)
    password = models.CharField(max_length=128)
    user_birth = models.DateTimeField()
    user_gender = models.CharField(max_length=1)
    reg_dt = models.DateTimeField(auto_now_add=True)
    mod_dt = models.DateTimeField(null=True, blank=True)
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    del_yn = models.CharField(max_length=1, default='N')
    auto_login_yn = models.CharField(max_length=1, default='N')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # 추가된 필드

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['user_nickname']

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def user_seq_str(self):
        return str(self.user_seq)

    class Meta:
        db_table = 'user'
        managed = False


class DietPeriod(models.Model):
    diet_period_seq = models.AutoField(primary_key=True)
    user_seq = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_seq')
    start_dt = models.DateTimeField(auto_now_add=True)
    goal_dt = models.DateTimeField()
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    goal_weight = models.FloatField(default=0.0)
    period = models.IntegerField(null=True, blank=True)
    bmr = models.IntegerField(null=True, blank=True)
    tdee = models.IntegerField(null=True, blank=True)
    total_kcal = models.IntegerField(null=True, blank=True)
    daily_kcal = models.IntegerField(null=True, blank=True)
    daily_carbo = models.IntegerField(null=True, blank=True)
    daily_protein = models.IntegerField(null=True, blank=True)
    daily_prov = models.IntegerField(null=True, blank=True)
    reg_dt = models.DateTimeField(auto_now_add=True)
    stop_dt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'diet_period'