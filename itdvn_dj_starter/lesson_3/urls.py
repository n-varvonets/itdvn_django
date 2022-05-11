from django.urls import path
from lesson_3 import views

urlpatterns = [
    path('main/', views.main),
    path('main/text/', views.text, name='text'),
    path('main/file/', views.file, name='file'),
    path('main/redirect/', views.redirect, name='redirect'),
    path('main/not_allowed/', views.not_allowed, name='not_allowed'),
    path('main/json/', views.json, name='json'),
]
