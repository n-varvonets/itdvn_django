from datetime import datetime, timedelta

from django.db import models

# Создадим 3 модели для цветочного магазина (клиент, цветок, букет)


class Flower(models.Model):
    count = models.IntegerField(default=0, blank=True)  # по умолчанию у нас нет ТАКИХ цветков, но так же есть возможность указать пустое поле
    description = models.TextField(null=True)  # если при создании мы укажем пустое, то автоматом в бд запишется Null
    # delivered_at = models.DateTimeField(default=datetime.now(), blank=True)  # 1ый способ добавить дату доставки через datetime
    delivered_at = models.DateTimeField(auto_now_add=True, blank=True)  # 2ой способ через models - это более правильно, т.к. нет необходимости импорта доп. модулей
    could_use_in_bouquet = models.BooleanField(default=True)  # может ли данный цветок быть использован в букете
    wiki_page = models.URLField(default='https://ru.wikipedia.org/', unique_for_date="delivered_at")  # укажем на линк описания нашего цветка в википедии, \
    # по дефолту укажем саму википедию + unique_for_date говорит что поле wiki_page должно быть уникально для этой даты delivered_at(их комбинация)
    name = models.CharField(max_length=64, unique=True)  # для CharField есть ОБЬЯЗАТЕЛЬНЫЙ аттрибут max_length + укажем что название цветка - уникально

# При blank=True, проверка данных в форме позволит сохранять пустое значение в поле. При blank=False поле будет обязательным.


class Bouquet(models.Model):
    fresh_period = models.DurationField(default=timedelta(days=5),
                                        help_text='Use this field when you need info about bouquet time duration')  # указываем \
    # сколько времени наш букет может быть свежим, по дефолту будет свежим 5ть дней с момента создания. help_text  отображаться  в админ панели и в форму
    photo = models.ImageField(blank=True, null=True)  # задаем картинку, может быть пустым()
    price = models.FloatField(default=1.0)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # сделаем так
    second_email = models.EmailField()
    name = models.CharField(max_length=64)
    invoice_doc = models.FileField()  # это наша накладная
    user_uuid = models.UUIDField(editable=False)  # его уникальное значение укажем что нельзя изменять
    discount = models.DecimalField(max_digits=10, decimal_places=3)  # т.е. мы точно знаем что наша акция НЕ ДОЛЖНА быть БОЛЬШЕ чем 10%. decimal_places - колво цивер после запятой, max_digits - всего доступно цифер
    client_ip = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")  # определим ip нашего клиента
