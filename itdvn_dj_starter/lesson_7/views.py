import os.path

from django.urls import reverse_lazy
from django.views.generic import FormView

from itdvn_dj_starter import settings
from django.shortcuts import render
from lesson_7.forms import MyForm, FormModelClient
from django.http import HttpResponse


# def my_form(request):
#     """данная функция как пример вывода формы на страницу, НО без html и возможности сохранить в бд"""
#     return HttpResponse(MyForm().as_p())  # .as_p() - позволяет выводить нашу форму в теге <p>, т.е. вместе с названиями полей
#     так же есть .as_table() - мы используем его в form_page.html

def my_form_GET(request):
    """В отличие от верхней функции добавим возможность сохранять данные в бд и отображать html клиенту"""
    form = MyForm(request.GET or None)  # сохраняем в инстанс результат работы формы по GET запросу клиента. \
    # Как это работает? Просто отправляется два раза: \
    # - первый раз ДЛЯ клиента - пустой dict с полями, что бы он заполнить её; \
    # - второй раз ОТ клиента - что бы его могли обработать. \
    # Это легко проверить следующим принтом... первый раз выводится принт для клиента с пустым dict, \
    # второй раз отобразится принт от клиента с данными.
    # "or None" убирает со страницы надписи у поля Required - тем самым уберем лишние надписи
    print(request.GET)
    # >>> <QueryDict: {}>   - это до кнопки submit клиентом
    # >>> <QueryDict: {'name': ['Me'], 'email': ['klenova1616@gmail.com'], 'age': ['pia3.py'], 'agreement': ['on'], 'average_score': ['5']}>
    # >>> [13/May/2022 08:57:29] "GET /lesson_7/my_form/?name=Me&email=klenova1616%40gmail.com&age=pia3.py&agreement=on&average_score=5 HTTP/1.1" 200 755
    # + в логах видно что это GET запрос и наши данные отображаются в url - что плохо, надо post

    # добавим мощный механизм формы - проверку данных .is_valid() и ее НОМРАЛИЗАЦИЮ. к примеру выше в url agreement=on \
    # а в cleaned_data это поле будет типом для пайтона "agreement": True
    if form.is_valid():
        print(form.cleaned_data)
        print(form.errors)  # если зайдет в true, то errors будет пустым
    else:
        print(form.cleaned_data)  # отобразится все корректные данные, за исключение ошибок
        print(form.errors)  # отобразится конкретное поле ошибки

    return render(request, 'form_page.html', context={'form': form})


def my_form_post(request):
    """
    Недостаток метода выше - это что отправляется GET запрос и атрибуты идут в параметрах url.
    Изменим ту же логику с теми же формами, но уже c POST методом.
    Для этого во form_page.html изменим тег form на POST + csrf_token и здесь во views...:
    """
    form = MyForm(request.POST or None)
    print("post ", request.POST)
    # >>> post  <QueryDict: {'csrfmiddlewaretoken': ['0zWk83wXq7NxHmjnJtRF5A8ldNl1tlW8s75TOLvqCMQH3CE8rjWvALCoVbLhnBxC'], \
    # 'email': ['qeweqw@qaswe.com'], 'password': ['123213214235231563'], 'age': ['15'], 'average_score': \
    # ['10.1']}>  <ul class="errorlist"><li>name<ul class="errorlist"><li>This field is required.</li></ul></li></ul> \
    # - с таким обьектом мы работаем в нашем скрипте

    # ВАЖНО: что в логах url уже не отображается пароль при методе post  csrf_token
    # [13/May/2022 12:04:18] "POST /lesson_7/my_form/?name=Me&email=klenova1616%40gmail.com&age=herding-cats.gif&agreement=on&average_score=5 HTTP/1.1" 200 1211
    if form.is_valid():
        print("cleaned_data", form.cleaned_data)
        print(form.errors)
    else:
        print("err", form.errors)

    return render(request, 'form_page.html', context={'form': form})


def my_form(request):
    """К прошлой POST форме добавим возможность записывать файлы"""
    print(request.FILES)  # просмотрим файлы, которые будут отправляться в нашем request от клиента
    # <MultiValueDict: {'profile_picture': [<InMemoryUploadedFile: photo_2021-08-02_12-20-35.jpg (image/jpeg)>], 'additional_file': [<InMemoryUploadedFile: few_structed_startups.json (application/json)>]}>
    form = MyForm(request.POST or None, request.FILES or None)  # создаем экземпляр нашей формы

    if form.is_valid():
        print('cleaned_data ', form.cleaned_data)

        img_file_path = os.path.join(
            settings.MEDIA_ROOT, form.cleaned_data['profile_picture'].name
        )  # создадим файл(без данных по указанному дир и с определенным названием) загружать полученные файлы в дир MEDIA_ROOT,\
        # т.е. в lesson_5/static/tmp... , а вторым параметром - название файла, который будет в нашем request

        with open(img_file_path, 'wb+') as local_file:  # открываем только что созданный пустой файл и записуем в него данные
            for chunk in form.cleaned_data['profile_picture']:  # ВАЖНО!!!!!!!!!: цикл для того что бы если большой файл, \
                # то что бы не нагружать нашу систему - будем записывать его по кускам - просто напросто не будет приходить в request.FILES
                local_file.write(chunk)  # в наш файл будем дописывать те файлы, которые придут с нашего request

        # тоже самое проделываем и для File делываем
        file_path = os.path.join(
            settings.MEDIA_ROOT, form.cleaned_data['additional_file'].name
        )
        with open(file_path, 'wb+') as local_file:
            # ВАЖНО!!!!!!!!!: в цикле, а то просто напросто не будет приходить в request.FILES
            for chunk in form.cleaned_data['additional_file']:
                local_file.write(chunk)
    else:
        print("errors", form.errors)

    return render(request, 'form_page.html', context={'form': form})


class MyFormView(FormView):
    """Тоже самое можно сделать что и в my_form но уже более абстрактно"""
    form_class = MyForm
    template_name = 'form_page.html'

    def get(self, request, *args, **kwargs):
        print(request.GET)  # - будет отображаться форма, но нужно здесь прописать логику сохранения файлов
        return super().get(request, *args, **kwargs)


class ModelFormClientView(FormView):
    """Наиболее встречающий вариант создания формы 'на лету' из полей модели"""
    form_class = FormModelClient
    template_name = 'form_page.html'
    success_url = reverse_lazy('modelform')  # будем перенаправлять на ту же страницу на которой отправили. \
    # name='modelform' из my_drf_urls.py

    # данная форма даже сохранеет файлы в дир что указана  MEDIA_ROOT

    def form_valid(self, form):
        """Данный метод вызывается когда форма была провалидирована"""
        form.save()  # перед тем как перейти на get_success_url() в ниже методе - нам нужно сохранить данные с формы в модель
        return super().form_valid(form)


