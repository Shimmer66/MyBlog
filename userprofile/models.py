from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True,default='')
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=200, blank=True)
    last_logindate = models.DateTimeField(auto_now=True)
    sign_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return 'user {}'.format(self.user.username)


