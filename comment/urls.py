from django.urls import path
from . import views
app_name='comment'
urlpattrens=[
    path('comment/<int:article_id>/',views.comment,name='comment')
]