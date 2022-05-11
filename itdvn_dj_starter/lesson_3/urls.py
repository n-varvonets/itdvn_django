from django.urls import path
from lesson_3 import views
from lesson_3.post_view import index_post, post_page, MyTemplateView

urlpatterns = [
    path('main/', views.main),
    path('main/text/', views.text, name='text'),
    path('main/file/', views.file, name='file'),
    path('main/redirect/', views.redirect, name='redirect'),
    path('main/not_allowed/', views.not_allowed, name='not_allowed'),
    path('main/json/', views.json, name='json'),

    path('class-view/', views.MyView.as_view(), name='class_view'),
    # если мы наш класс от views.py наследуем от View, то наш класс будет иметь метод as_view(),
    # после чего вызывается метод dispatch() - того что бы определить какой метод вызвался()

    # используем новый файл view - post_view. сверху импортируем конкретные функции
    # path('post/', index_post, name='index_post'),  # рабочая урл через функцию
    path('post/', MyTemplateView.as_view(), name='index_post_template_view'),  # тот же самый функционал, но через TemplateView
    path('post/<int:number>/', post_page, name='post_page'),
]
