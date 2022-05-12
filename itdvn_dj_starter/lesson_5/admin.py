from django.contrib import admin
from lesson_5.models import Flower, Bouquet, Client

# зарегистрируем наши модели

admin.site.register(Flower)
admin.site.register(Bouquet)
admin.site.register(Client)
