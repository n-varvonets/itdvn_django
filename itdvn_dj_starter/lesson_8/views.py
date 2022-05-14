from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q

import csv
import datetime

from lesson_8.models import GameModel, GamerLibraryModel, GamerModel

# ORM - технология програмирования, которая связывает бд с концепциями оо(языков)п
# QuerySet - позволяет читать данные из бд. QuerySet не работает напрямую с бд, т.е. с ним можно работать без фактического \
# запроса к бд. QuerySet создает "ленивые запросы" - можно фильтровать, обрезать, сортировать не выполняя запросы к бд.


def upload_data(request ):
    """метод для загрузки данных в бд. для того что в бд были данные для того что бы делать QuerySet"""
    with open('vgsales.csv') as f:  # условная данные для бд: 1,Wii Sports,Wii,2006,Sports,Nintendo,41.49,29.02,3.77,8.46,82.74
        reader = csv.reader(f)
        for row in reader:
            print(row)
            try:
                _, created = GameModel.objects.get_or_create(
                    name=row[1],
                    platform=row[2],
                    year=datetime.date(int(row[3]), 1, 1),
                    genre=row[4],
                    publisher=row[5],
                    na_sales=row[6],
                    eu_sales=row[7],
                    jp_sales=row[8],
                    other_sales=row[9],
                    global_sales=row[10],
                )  # если нет записи, то создает новую, если есть, то берет и помещает в _      + авто сохраняет
            except:
                print(f'{row} is skipped')

    return HttpResponse("Done!")


class FilterGameView(ListView):
    """
    ListView - для того что бы отобразить много элементов + уже есть абстрактный параметр queryset, который переопределяем.
    Плюсы в том что не нужно ничего возвращать, а только лишь указать:
        - template_name;
        - queryset.
    В template_name автоматически передастся queryset, как object_list(но можно изменить это название)
    """
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.filter(name="Hitman (2016)")


class ExcludeGameView(ListView):
    """
    Как видно можно использовать один темплейт(gamemodel_list.html) для нескольких представлений(FilterGameView и ExcludeGameView)
    """
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.exclude(name__contains="Hitman")  # исключаем все темплейт, где аттрибут содержит в себе \
    # минимальное совпадение через суфикс "__contains"


class AvailableFiltersView(ListView):
    """
    Примеры работы с параметрами фильтра.
    Структура: Имя_поля__фильтр
    Более подробно в презентации в этой директории
    """
    template_name = 'gamemodel_list.html'
    # queryset = GameModel.objects.filter(name__in=["Hitman (2016)", "Tetris"])  # отобразит 2 игры с точным названием поля
    # queryset = GameModel.objects.filter(na_sales__gt=20)  # отобразит в элементы, у которых скидка больше чем(__gt)
    # queryset = GameModel.objects.filter(na_sales__lte=0.5)  # отобразит в элементы, у которых скидка меньше чем или равно(__lte)
    # queryset = GameModel.objects.filter(name__startswith="Hitm")  # отобразит в элементы, которые начинаются с Hitm
    # queryset = GameModel.objects.filter(na_sales__range=range(1, 3))  # отобразит в элементы, которые находятся в диапазоне чисел
    # queryset = GameModel.objects.filter(year__year=2000)  # позволяет фильтровать по дате(год, месяц, день). Поле должно быть типа date
    # queryset = GameModel.objects.filter(name__isnull=True)  # отобразит все записи у которых name == null
    queryset = GameModel.objects.filter(name__regex=r'^(An?|The) +')  # отобразит все записи которые начинаются на An или The


class ComplexQFiltersView(ListView):
    """Составные запросы с оператором OR, AND, NOT используются с объектом Q - инкапсулирует множества именованных аргументов"""
    template_name = 'gamemodel_list.html'
    # queryset = GameModel.objects.filter(
    #         Q(name__startswith="A") & Q(name__endswith="a") & Q(name__contains="ma")
    #     )  # & - оператор AND, т.е. наша игра должна начинаться с "А" и заканчиваться на "а", так же должна иметь в себе "ma"

    # queryset = GameModel.objects.filter(
    #     Q(name__startswith="Ab") | Q(name__endswith="Ad") | Q(name__contains="Mat")
    # )  # | оператор ИЛИ

    queryset = GameModel.objects.filter(
        ~Q(name__startswith="Ab") | ~Q(name__endswith="Ad") | ~Q(name__contains="Mat")
    )  # ~ - знак отрицания, т.е Не должна начинаться на "Ab" ИЛИ НЕ должно заканчиваться на "Ad" ИЛИ НЕ ...


class OrderedByView(ListView):
    """Пример сортировки данных"""
    # к примеру отсоритруем все игры название с Hitman в обратном порядке
    template_name = 'gamemodel_list.html'
    # queryset = GameModel.objects.filter(name__contains="Hitman").order_by('-year')  # - перед говорит отсортировать в обратном порядке
    queryset = GameModel.objects.filter(name__contains="Hitman").order_by('year').reverse()  # ну или тот же самый результат, \
    # только с применением  .reverse()


class AllView(ListView):
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.all()


class UnionView(ListView):
    """Метод объединяет несколько queryset, НО одним запросом. ORM ратиться к бд, когда html потребует отобразить"""
    # например мы ищем из всего списка данных две игры:
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.filter(name="Hitman (2016)").union(
        GameModel.objects.filter(name="Tetris"))


class NoneView(ListView):
    template_name = 'gamemodel_list.html'
    queryset = GameModel.objects.none()


class ValuesView(ListView):
    template_name = 'gamemodel_list.html'

    queryset = GameModel.objects.filter(name="Hitman (2016)").values("name",
                                                                     "platform",
                                                                     "year")  # используется что бы вытянуть КОНКРЕТНЫЕ поля

    def get(self, request, *args, **kwargs):
        """
        т.к. в ListView используется один queryset, то для примера получения значений переопределим метод get,
        где продемонстрируем примеры
        """
        print(GameModel.objects.filter(name="Hitman (2016)").values("name",
                                                                    "platform",
                                                                    "year"))

        # >>> <QuerySet [{'name': 'Hitman (2016)', 'platform': 'PS4', 'year': datetime.date(2016, 1, 1)}, {'name': \
        # 'Hitman (2016)', 'platform': 'XOne', 'year': datetime.date(2016, 1, 1)}]>

        print(list(
            GameModel.objects.filter(name="Hitman (2016)").values_list("name", "platform", 'year')))
        # [('Hitman (2016)', 'PS4', datetime.date(2016, 1, 1)), ('Hitman (2016)', 'XOne', datetime.date(2016, 1, 1))]

        return super().get(request, *args, **kwargs)


def date_view(request):
    data = GameModel.objects.filter(name__contains="Hitman").dates(field_name='year', kind='year')  # kind - указывает на элемент\
    # по который мы  будет обрезать нашу дату
    print(data)
    # >>> <QuerySet [datetime.date(2002, 1, 1), datetime.date(2003, 1, 1), datetime.date(2004, 1, 1), datetime.date(2006, 1, 1), \
    # datetime.date(2007, 1, 1), datetime.date(2008, 1, 1), datetime.date(2009, 1, 1), datetime.date(2010, 1, 1), \
    # datetime.date(2012, 1, 1), datetime.date(2013, 1, 1), datetime.date(2016, 1, 1)]> - единицы обрезаются на странице
    return HttpResponse(data)


def get_view(request):
    # можно получить ТОЛЬКО ОДНУ запись(как правило, уникальный id записи)
    data = GameModel.objects.get(id=27)
    print(data)
    return HttpResponse(data)


def create_view(request):
    # """Ниже будут описаны разные подходы создания таблиц и их записей. (плюсы минусы)"""
    # # ВАЖНО!:
    # #   - ТОЛЬКО при вызове save() django обращается к бд
    # #   - save() не возвращает инстанс
    # #   - поддерживает связь ForeignKey, M2M
    #
    #
    # print('~~~ 1.) Первый подход: класс- это модель, экземпляр - это запись таблицы ~~~')
    #
    # # 1.1) через атрибуты записи(экземпляр)
    # myself_1_1 = GamerModel()
    # myself_1_1.email = "1_1_admin@admin.com"
    # myself_1_1.nickname = "1_1_SomeRandomNicknameSave"
    # myself_1_1.save()
    #
    # # 1.2) Тот же подход, но через парметры и используя .save()
    # myself_1_2 = GamerModel(email="1_2_admin@admin.com",
    #                     nickname="1_2_SomeRandomNicknameSave")
    # myself_1_2.save()
    #
    # # 1.3) Через параметры используя dict
    # myself_1_3 = GamerModel(**{"email": "1_3_admin@admin.com",
    #                        "nickname": "1_3_SomeRandomNicknameSave"})
    # myself_1_3.save()
    #
    # print('~~~ 2.) Второй подход: используя МЕНЕДЖЕРА и  метод create() ~~~')
    # # ВАЖНО!!!:
    # #   - не работает со связями ForeignKey, M2M
    # #   - если id заполняется через AutoField, то его значение не будет получено(pk), как это делает метод save()
    # #   - он работает быстрее чем .save()
    #
    # # 2.1) через dict и kwargs
    # myself_2_1 = GamerModel.objects.create(**{"email": "2_1_admin@admin.com",
    #                                       "nickname": "2_1_SomeRandomNicknameCreate"})
    #
    # # 2.2) через обычные параметры
    # myself_2_2 = GamerModel.objects.create(email="2_2_admin@admin.com",
    #                                    nickname="2_2_SomeRandomNicknameCreate")
    #
    # # 2.3) Множество обьектов одним запросом
    # myself_2_3 = GamerModel.objects.bulk_create([
    #     GamerModel(
    #         email="2_3_admin@1admin.com", nickname="2_3_SomeRandomNicknameBulkCreate1"),
    #     GamerModel(
    #         email="2_3_admin@2admin.com", nickname="2_3_SomeRandomNicknameBulkCreate2"),
    #     GamerModel(
    #         email="2_3_admin@3admin.com", nickname="2_3_SomeRandomNicknameBulkCreate3"),
    #     GamerModel(
    #         email="2_3_admin@4admin.com", nickname="2_3_SomeRandomNicknameBulkCreate4")
    # ])
    #
    # print('~~~ 3.) Третий подход: создавать модели, когда у нас есть связи в моделях (ForeignKey, M2M) ~~~')
    # # GamerLibraryModel имеет 3 аттрибута (game=M2M, gamer=ForeignKey, size)
    #
    # my_library = GamerLibraryModel(gamer=GamerModel.objects.get(pk=10),
    #                                size=10)  # создание нашей записи (пока без поля M2M)
    # my_library.save()  # сохраним нашу модель.
    # # Т.е. на данном этапе public.lesson_8_gamerlibrarymodel имеет поля:(http://i.imgur.com/wmLFwfT.png)
    # #   - id (наш pk модели GamerLibraryModel)
    # #   - size(наше обычное поле)
    # #   - gamer_id(ForeignKey геймеру)
    # #   - нет поля М2М, сейчас создадим его связь(сколько угодно раз к сколько угодно фильмам через новую таблиц \
    # #   lesson_8_gamerlibrarymodel_game с полями id, gamerlibrarymodel_id, gamemodel_id - http://i.imgur.com/bHiuNyW.png)
    # my_library.game.set([GameModel.objects.get(pk=1),
    #                      GameModel.objects.get(pk=2),
    #                      GameModel.objects.get(pk=3)])  # к нашему инстансу добавим отношение M2M, а именно \
    # # в значение game установим 3 первые игры.
    # # ИТОГО: модель public.lesson_8_gamerlibrarymodel, так и осталась без измений(с 3мя полями: id, size, gamer_id), а вот \
    # # в новой связующей модели lesson_8_gamerlibrarymodel_game создались 3 записи с единым id инстанса и \
    # # разными id игр http://i.imgur.com/V7MpTZ0.png
    #
    # # 3.2) создание массива M2M (bulk_create)
    # my_library = GamerLibraryModel.objects.bulk_create(
    #     [GamerLibraryModel(gamer=GamerModel.objects.get(pk=15),
    #                        size=9),  # создаем для геймера с id 15
    #      GamerLibraryModel(gamer=GamerModel.objects.get(pk=18),
    #                        size=10)  # и геймера с id 18
    #      ])  # таким образом мы создали одним запросом 2 модели для lesson_8_gamerlibrarymodel, НО \
    # # нет возможности указать через bulk_create M2M, поэтому дальше указываем эту связь поодиночно(как в примере выше)

    # 4)Пример изменения одного аттрибута
    # 4.1) первый способ через get и .save()
    my_friend = GamerModel.objects.get(pk=18)
    my_friend.nickname = "MySecondNickname_1"
    my_friend.save()
    # 4.2) второй способ через .filter() и .update()
    my_friend_2 = GamerModel.objects.filter(pk=19)
    my_friend_2.update(nickname="MySecondNickname_2")  # update только с  QuerySet

    return HttpResponse(my_friend, my_friend_2)

