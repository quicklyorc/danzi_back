import os
import django
from django.conf import settings

# 환경 변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django 설정 초기화
django.setup()

# 나머지 코드 작성
from django.db import connection
from django.core.management import call_command

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app='admin';")
    cursor.execute("DELETE FROM django_migrations WHERE app='auth';")
    cursor.execute("DELETE FROM django_migrations WHERE app='authtoken';")
    # cursor.execute("DELETE FROM django_migrations WHERE app='contenttypes';")
    cursor.execute("DELETE FROM django_migrations WHERE app='sessions';")
    cursor.execute("DELETE FROM django_migrations WHERE app='user';")
    cursor.execute("DELETE FROM django_migrations WHERE app='diet';")

call_command('migrate', 'admin', '0001_initial')
call_command('migrate', 'auth', '0001_initial')
call_command('migrate', 'authtoken', '0001_initial')
# call_command('migrate', 'contenttypes', '0001_initial')
call_command('migrate', 'sessions', '0001_initial')
call_command('migrate', 'user', '0001_initial')
call_command('migrate', 'diet', '0001_initial')
