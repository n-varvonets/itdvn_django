from django.urls import path
from lesson_5 import views

urlpatterns = [
    path('create_flower/', views.create_flower, name='create_flower'),
    path('create_client/', views.create_client, name='create_client'),
    path('get_bouquet_price/', views.get_bouquet_price, name='get_bouquet_price'),
]
