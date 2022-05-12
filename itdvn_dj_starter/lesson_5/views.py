from uuid import uuid4  # добавляет рандомный id в виде 9ae000cd-1e52-4e00-a889-8f4d0c48314d
from django.shortcuts import render
from lesson_5.models import Flower, Bouquet, Client
from django.http import HttpResponse
from decimal import Decimal
from django.core.files import File
from django.contrib.auth.models import User  # User жен быть зарегистрирован, таким образом мы можем связаться зарегистрированного \
# юзера с клиентом или оставить его анонимным как просто из раздела lessson_5


def create_flower(request):
    rose = Flower()
    rose.count = 5
    rose.description = "Растение с красивыми крупными душистыми цветками и со стеблем, обычно покрытым шипами"
    rose.could_use_in_bouquet = True
    rose.wiki_page = "https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D0%B7%D0%B0"
    rose.name = "Роза"
    # delivered_at и id  сами автоматически добавятся
    rose.save()
    return HttpResponse(f"Flower {rose.name} is created!")

# ----------------- 2ой способ добавления объектов через objects --------------------


def create_client(request):
    with open('../requirements.txt', 'r') as _file:  # для примера файл наш нашей накладной
        tmp_file = _file.read()

    client = Client.objects.create(**{
        'user': User.objects.get(pk=1),  # если это поле не указывать, то мы просто создадим неаутентифицированного клиента для \
        # раздела lesson_5. http://i.imgur.com/6u6Jv9J.png.  бы указать что наш клиент является аутентифицированным юзером, то \
        # то его с помощью этой строки можно связать с уже существующим \
        # (для это мы создали суперпользователя python manage.py createsuperuser и его id=1, т.е. pk=1)
        'second_email': 'nick_admin@admin1.com',
        'name': 'Nick_auth_admin_as_client',
        # 'invoice_doc': tmp_file,
        'invoice_doc': File(open('../requirements.txt'), 'some_filename'),  # то же самое что и выше, но только с  \
        # from django.core.files import File. - это позволяет вместо того что бы хранить файл в бд - то в данной дир создадим \
        # новую дир static/tmp в которую будут помещаться наши файлы. Для этого в settings.py нужно добавить путь к ней в \
        # переменную MEDIA_ROOT + добавить в models.py к этому аттрибуту upload_to='uploads/%Y/%m/%d/' паттерн, который будет \
        # создавать подобное дерево. Первым параметром передаем файл, вторым - его название
        'user_uuid': uuid4(),
        'discount': Decimal("20.0785468"),
        'client_ip': '127.0.0.1',
    })
    return HttpResponse(f"Client {client.name} was created")


def get_bouquet_price(request):
    price_bouquet = Bouquet.shop.get(id=1).price
    return HttpResponse(f"Flower price is {price_bouquet}")


