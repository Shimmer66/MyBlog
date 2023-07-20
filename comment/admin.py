from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Comment

# Register your models here.
admin.site.register(Comment,verbose_name='评论')