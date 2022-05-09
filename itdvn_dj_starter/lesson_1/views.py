from django.http import HttpResponse
from django.shortcuts import render  # render - позволяет через html ответить на http запрос


# def index(request):
#     """простой ответ"""
#     return HttpResponse('Fuck the world!')

def index(request):
    """html ответ"""
    return render(request, 'index_1.html', {})  # будем отправлять тот же request(который к нам пришел), '' - наш html, {} - наш конекст диктшинари