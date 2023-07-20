import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
print(LOG_DIR)
z = os.path.join(LOG_DIR, 'django.log')
print(z)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  # 媒体文件在服务器上的实际存储位置
print(MEDIA_ROOT)
