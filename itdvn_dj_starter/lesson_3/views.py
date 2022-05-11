from django.http import HttpResponse, FileResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static


def main(request):
    print(request)
    # return HttpResponse('<button>My button of html</button>')  # просто на страничке будет отображаться одна кнопка
    return render(request, 'main.html')  # подгрузит целую страницу со всеми ниже функциями в одной(описываем структуру в templates)


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


