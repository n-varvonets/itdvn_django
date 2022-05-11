from django.http import HttpResponse, FileResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.generic import View

from django.template import loader


def main(request):
    test_template = loader.render_to_string('template_example.html',
                                            context={'test_key': "test_value"}
                                            )
    return HttpResponse(test_template)

    # 2ой промежуточный способ
    # test_template = loader.get_template(template_name='template_example.html')
    # print(test_template, type(test_template), '\n', test_template.render)
    # return HttpResponse(test_template.render())

    # 3ий начальный способ
    # return render(request, 'template_example.html')  # подгрузит целую страницу со всеми ниже функциями в одной(описываем структуру в templates)


def text(request):
    return HttpResponse('Just simply text')


def file(request):
    # with open() as file:
    #     work with file - это все уже не нужно т.к. имеем FileResponse
    print(static('img/001.jpg'))
    return FileResponse(open(static('img/001.jpg'), 'rb+'))


def redirect(request):
    return HttpResponseRedirect('https://www.google.com/')


def not_allowed(request):
    return HttpResponseNotAllowed('You shall not pass!!!')


def json(request):
    return JsonResponse({i: i * i for i in range(1, 20)}, safe=False)  # safe -


# Пример реализиций Function vs Class
def my_view_example(request):
    if request.method == "GET":
        # <view logic>
        return HttpResponse('result')


class MyViewExample(View):
    # метод dispatch() определяет какой метод вызвался клиентом из доступных(get,post... - можно внутри View эт просмотреть).
    # если пришел запрос методом post, а в этом классе он не определен, то тогда будет ошибка
    def get(self, request):
        # <view logic>
        return HttpResponse('result')


class MyView(View):

    def get(self, request):
        print(request.GET)
        # >>> <QueryDict: {'csrfmiddlewaretoken': ['eO03CjCqIS4FFdcK7Tp4LDdXrTvTNdsCX321xHXRajnnmRmVLDdWugpzI809bNyf'], 'this_is': ['POST'], 'type': ['json']}>
        """добавим логику"""
        if request.GET.get('type') == "file":
            return FileResponse(open(static('img/001.jpg'), 'rb+'))
        elif request.GET.get('type') == "json":  # alert ajax  не разрешает выводить json или редиректить, но иснфу мы можем получить
            return JsonResponse(list({i: i * i for i in range(1, 20)}), safe=False)
        elif request.GET.get('type') == "redirect":
            # return HttpResponseRedirect('https://www.google.com/')  #  не подойдет, потому что использует какуе-то кофнидициальность
            return HttpResponseRedirect('http://127.0.0.1:8000/lesson_3/main/')# но мы всегда можем редирекнуть юзера по нашему сайту
        else:
            return HttpResponseNotAllowed('You shall not pass!!!2222')
        # return HttpResponse('This is get')

    def post(self, request):
        print(request.POST)
        return HttpResponse('This is post')


