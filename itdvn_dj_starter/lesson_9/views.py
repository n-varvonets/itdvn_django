from lesson_8.models import GameModel, GamerModel
from rest_framework import viewsets
from lesson_9.serializers import GameModelSerializer, GamerModelSerializer


# с прошлого урока забираем наши модели(GameModel, GamerModel) по которым будем делать запросы в бд

class GameViewSet(viewsets.ModelViewSet):
    queryset = GameModel.objects.all().order_by('-year')
    serializer_class = GameModelSerializer


class GamerViewSet(viewsets.ModelViewSet):
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer
