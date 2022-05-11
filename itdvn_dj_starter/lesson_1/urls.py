from django.urls import path
from lesson_1 import views

urlpatterns = [
    path('index/', views.index, name='lesson_1')
]
