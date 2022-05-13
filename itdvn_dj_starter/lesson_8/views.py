from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q

import csv
import datetime

from lesson_8.models import GameModel  # , GamerLibraryModel, GamerModel

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
    # myself = GamerModel()
    # myself.email = "admin@admin.com"
    # myself.nickname = "SomeRandomNicknameSave"
    # myself.save()

    # myself = GamerModel(email="admin@admin.com",
    #                     nickname="SomeRandomNicknameSave")
    # myself.save()
    #
    # myself = GamerModel(**{"email": "admin@admin.com",
    #                        "nickname": "SomeRandomNicknameSave"})
    # myself.save()

    # myself = GamerModel.objects.create(**{"email": "admin@admin.com",
    #                                       "nickname": "SomeRandomNicknameCreate"})

    # myself = GamerModel.objects.create(email="admin@admin.com",
    #                                    nickname="SomeRandomNicknameCreate")
    # myself = GamerModel.objects.bulk_create([
    #     GamerModel(
    #         email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate1"),
    #     GamerModel(
    #         email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate2"),
    #     GamerModel(
    #         email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate3"),
    #     GamerModel(
    #         email="admin@admin.com", nickname="SomeRandomNicknameBulkCreate4")
    # ])

    # my_library = GamerLibraryModel(gamer=GamerModel.objects.get(pk=10),
    #                                size=10)
    # my_library.save()
    # my_library.game.set([GameModel.objects.get(pk=1),
    #                      GameModel.objects.get(pk=2)])

    # my_library = GamerLibraryModel.objects.create(
    #     gamer=GamerModel.objects.get(pk=10),
    #     size=10)
    # my_library.game.set([GameModel.objects.get(pk=1),
    #                      GameModel.objects.get(pk=2)])

    # my_library = GamerLibraryModel.objects.bulk_create(
    #     [GamerLibraryModel(gamer=GamerModel.objects.get(pk=10),
    #                        size=10),
    #      GamerLibraryModel(gamer=GamerModel.objects.get(pk=10),
    #                        size=10)
    #      ])
    my_friend = GamerModel.objects.get(pk=10)
    my_friend.update(nickname="MySecondNickname")
    return HttpResponse(my_friend)