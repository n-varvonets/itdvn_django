from datetime import datetime, timedelta

from django.db import models

# Создадим 3 модели для цветочного магазина (клиент, цветок, букет)

# для psql важно добавить null=True(кроме M2M), для того чтобы при добавлении нового поля, не было пустых значений и при миграции\
# psql не приходилось перезагружать полностью таблицу(смотри в 006_презентации и преимущества/недостатки бд), а то будет медленно


class Flower(models.Model):
    count = models.IntegerField(default=0, blank=True, null=True)  # по умолчанию у нас нет ТАКИХ цветков, но так же есть возможность указать пустое поле
    description = models.TextField(null=True)  # если при создании мы укажем пустое, то автоматом в бд запишется Null
    # delivered_at = models.DateTimeField(default=datetime.now(), blank=True)  # 1ый способ добавить дату доставки через datetime
    delivered_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # 2ой способ через models - это более правильно, т.к. нет необходимости импорта доп. модулей
    could_use_in_bouquet = models.BooleanField(default=True, null=True)  # может ли данный цветок быть использован в букете
    wiki_page = models.URLField(default='https://ru.wikipedia.org/', unique_for_date="delivered_at", null=True)  # укажем на линк описания нашего цветка в википедии, \
    # по дефолту укажем саму википедию + unique_for_date говорит что поле wiki_page должно быть уникально для этой даты delivered_at(их комбинация)
    name = models.CharField(max_length=64, unique=True, null=True)  # для CharField есть ОБЬЯЗАТЕЛЬНЫЙ аттрибут max_length + укажем что название цветка - уникально

# При blank=True, проверка данных в форме позволит сохранять пустое значение в поле. При blank=False поле будет обязательным.


class Bouquet(models.Model):
    shop = models.Manager()  # таким образом для получения queryset с бд мы заменили objects на shop
    fresh_period = models.DurationField(default=timedelta(days=5), null=True,
                                        help_text='Use this field when you need info about bouquet time duration')  # указываем \
    # сколько времени наш букет может быть свежим, по дефолту будет свежим 5ть дней с момента создания. help_text  отображаться  в админ панели и в форму
    photo = models.ImageField(blank=True, null=True)  # задаем картинку, может быть пустым()
    price = models.FloatField(default=1.0, null=True)
    flowers = models.ManyToManyField(Flower, verbose_name="This bouquet consist of this flowers")  # т.е. цветы, которые могут \
    # входить в данный букет, из чего он состоит. В параметрах нужно указать название класса с которым будет отношение


# Джанго уже имеет внутри модель Юзер(т.к. он везде применяется) с уже созданными полями. Если пройти внутрь импортированного \
# объекта, то можно увидеть его аттрибуты
from django.contrib.auth.models import User


class Client(models.Model):
    """
    Применим прием UserProfile:
    Переопределим buildin модель User с нашими аттрибутами используя  user = models.OneToOneField,
    а дальше задаем наши аттрибуты.
     """
    # id клиента будет добавляться автоматически
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # это будет ша связь между authed юзером и нашим созданным клиентом
    second_email = models.EmailField(null=True)
    name = models.CharField(max_length=64, null=True)
    invoice_doc = models.FileField(null=True, max_length=1000, upload_to='uploads/%Y/%m/%d/')  # это наша накладная, upload_to - \
    # это специфический паттерн, который позволит загружать файлы не в бд, а проект, смотри пример реализации в lesson_5/views.py
    user_uuid = models.UUIDField(editable=False, null=True)  # его уникальное значение укажем что нельзя изменять
    discount = models.DecimalField(max_digits=10, decimal_places=3, null=True)  # т.е. мы точно знаем что наша акция НЕ ДОЛЖНА быть БОЛЬШЕ чем 10%. decimal_places - колво цивер после запятой, max_digits - всего доступно цифер
    client_ip = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")  # определим ip нашего клиента
