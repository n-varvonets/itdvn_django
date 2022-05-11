from django.urls import path
from lesson_3 import views

urlpatterns = [
    path('main/', views.main),
    path('main/text/', views.text, name='text'),
    path('main/file/', views.file, name='file'),
    path('main/redirect/', views.redirect, name='redirect'),
    path('main/not_allowed/', views.not_allowed, name='not_allowed'),
    path('main/json/', views.json, name='json'),

    path('class-view/', views.MyView.as_view(), name='class_view')
    # если мы наш класс от views.py наследуем от View, то наш класс будет иметь метод as_view(),
    # после чего вызывается метод dispatch() - того что бы определить какой метод вызвался()
]
