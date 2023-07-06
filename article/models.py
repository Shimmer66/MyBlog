from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 作者，与 User 模型关联
    title = models.CharField(max_length=15)
    created_date = models.DateTimeField(auto_now_add=True)  # 创建日期，自动添加当前日期时间
    updated_date = models.DateTimeField(auto_now=True)  # 更新日期，自动更新为当前日期时间
    content = models.TextField()  # 文章内容
    article_type = models.CharField(max_length=50)  # 文章类型
    total_views = models.PositiveIntegerField(default=0)

    # 其他字段...
    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        db_table = 'Article'
        ordering = ('created_date',)

    def __str__(self):
        return self.title  # 返回文章标题

    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])
