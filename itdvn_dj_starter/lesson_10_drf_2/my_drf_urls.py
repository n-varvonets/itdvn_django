from django.urls import include, path
from lesson_10_drf_2 import views

from rest_framework import routers

# Для представлений типа ViewSet(т.к. это набор представлений уже есть функция(routers), которая \
# сама задает маршруты к ресурсу(обьекту), которые мы определил в представлении в файле views
router = routers.SimpleRouter()
router.register(r'view-set-example', views.VeiwSetAPIView)


urlpatterns = [

    path('', include(router.urls)),  # подключаем наш роутер от ViewSet

    path('veiw_function/', views.veiw_function, name='veiw_function'),
    path('apiview_class/', views.ClassAPIView.as_view(), name='apiview_class'),

    # для generic в отличие от ViewSet, т.к. это не набор представлений, то нам нужно указать каждый по отдельности вручную:
    path('generic_create/', views.MyCreateGenericAPIView.as_view(), name='generic_create'),
    path('generic_retrieve/<int:pk>', views.MyRetrieveGenericAPIView.as_view(), name='generic_retrieve'),
    path('generic_retrieve_update/<int:pk>', views.MyRetrieveUpdateGenericAPIView.as_view(), name='generic_retrieve_update'),

    # регистрация и аутентификация
    path('user_login/', views.user_login, name='user_login'),
    path('registration/', views.CreateUser.as_view(), name='registration'),

]

