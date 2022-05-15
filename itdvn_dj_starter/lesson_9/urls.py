from django.urls import include, path
from rest_framework import routers
from lesson_9 import views

router = routers.SimpleRouter()  # предоставляет CRUD(l) функционал к нашим ресурсам из созданных моделей_8_less -> views_les_9
router.register(r'game', views.GameViewSet)  # регистрируем ViewSet в роутер
router.register(r'gamer', views.GamerViewSet)

# добавляем наш роут в urls
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


