from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'


class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


