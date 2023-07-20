from django.db import models
from article.models import Article
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField(verbose_name='评论')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'

    def __str__(self):
        return self.body[:20]
