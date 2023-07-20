from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from PIL import Image


class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '文章栏目'
        verbose_name_plural = '文章栏目'



class Article(models.Model):
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article',
        verbose_name='栏目'
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='作者')  # 作者，与 User 模型关联
    title = models.CharField(max_length=15,verbose_name='标题')
    created_date = models.DateTimeField(auto_now_add=True)  # 创建日期，自动添加当前日期时间
    updated_date = models.DateTimeField(auto_now=True)  # 更新日期，自动更新为当前日期时间
    content = models.TextField(verbose_name='内容')  # 文章内容
    article_type = models.CharField(max_length=50,verbose_name='文章类型')  # 文章类型
    total_views = models.PositiveIntegerField(default=0,verbose_name='浏览量')
    title_image = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 其他字段...
    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        db_table = 'Article'
        ordering = ('created_date',)
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title  # 返回文章标题

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    def save(self, *args, **kwargs):
        article = super(Article, self).save(*args, **kwargs)
        if self.title_image and not kwargs.get('update_fields'):
            image = Image.open((self.title_image))
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.title_image.path)
        return article
