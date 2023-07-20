from django.contrib import admin
from .models import Article, ArticleColumn

# Register your models here.
admin.site.register(ArticleColumn)
admin.site.register(Article)
admin.site.site_header = '博客后台管理系统'
admin.site.site_title = '博客后台管理系统'