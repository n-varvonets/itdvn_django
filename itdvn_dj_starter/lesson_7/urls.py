from django.urls import path
from lesson_7 import views

urlpatterns = [
    path('my_form/', views.my_form, name='my_form'),
    path('class_form_abstract/', views.MyFormView.as_view(), name='class_form_abstract'),
    path('model_form/', views.ModelFormClientView.as_view(), name='modelform'),
]
