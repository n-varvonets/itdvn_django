# 1.)набор внешних модулей для реализации FunctionBasedView
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 2) набор внешних модулей для реализации APIView
from rest_framework.views import APIView

# 3) набор внешних модулей для реализации VeiwSetAPIView
from rest_framework import viewsets
from lesson_8.models import GameModel, GamerModel  # наши данные для queryset
from lesson_10_drf_2.serializers import GameModelSerializer, GamerModelSerializer  # для того что задать вид овтета
from rest_framework.generics import get_object_or_404

# 4) набор внешних модулей для реализации Generic - расширяет класс APIView, реализуя часто повторяющееся поведение. Т.е. если \
# наше представление подходит под стандартный шаблон CRUD(l)
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView

# 0) набор внешних модулей для реализации Регистрации, Аутентификации и авторизации пользователя
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK
from lesson_10_drf_2.serializers import UserSerializer  # импортируем модель-сериализтор для регистрации юзера

print('~~~ 0.)Регистрации, Аутентификации и авторизации пользователей ~~~~')
# 1) у нас должен быть url которому пользователь сможет создать профиль.(регистрация);
# 2) Предоставить нашему пользователю url, по которому он сможет создать сбе токен(логин)


@csrf_exempt  # декоратор используется для того что бы проверять csrf_token
@api_view(['POST'])  # указываем что функция логина только может вызывать метод пост
@permission_classes((AllowAny,))
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': 'Please, input username and password'})
    user = authenticate(username=username, password=password)  # авторизуем нашего пользователя в системе
    if not user:
        return Response({'error': 'Invalid data. Please, check correctness of data'})

    token, _ = Token.objects.get_or_create(user=user)  # джанго с коробки предоставлять таблицу/модель токенов(authtoken_token), \
    # в которую будем пробрасывать новый токен прикрепленного к конкретному пользователю(auth_user)
    return Response({'token': token.key}, status=HTTP_200_OK)


class CreateUser(CreateAPIView):  # используем обычный generic для создания новой записи
    permission_classes = (AllowAny,)  # в permission_classes нужно предать итерабильный обьект, в том числе \
    # можно и list, но сделал как tuple
    serializer_class = UserSerializer  # передаем сериализатор по модели которого будем создавать нового Authed user в базе


print('~~~ 1.) Пример реализации представления FunctionBasedView ~~~~')
@csrf_exempt
# @api_view()  # если использовать без параметров, тогда доступен будет только GET
@api_view(['GET', 'POST'])  # но есть возможность указать доп методы. На самой странице появится возможность добавить запись \
# и если это сделать, то в request.data будут отправленные данные, при get(): request.data={}
def veiw_function(request):
    print(request.data)
    return Response({'function': 'some_generated_data'})


print('~~~ 2.) Пример реализации представления APIView - основы, которую расширяют generics и ViewSet ~~~~')
class ClassAPIView(APIView):
    """работаем пока с методами(get,post), а не действиями(.list(), .create(), .retrieve(), update(), destroy())"""

    def get(self, request):
        return Response({'APIView_get': 'useful data by GET'})

    def post(self, request):
        print(request.data)
        request.data.update({"new_key": 'we can add any data to request and return it back'})  # к примеру мы можем добавить \
        # что угодно к возвращаемой инфе на странице после метода пост
        return Response(request.data)


print('~~~ 3.) Пример реализации представления ViewSet - основы, которую расширяют generics и ViewSet ~~~~')
class VeiwSetAPIView(viewsets.ViewSet):
    """
    Ресурс - наши Игры, т.е. модель GameModel
    VeiwSet. Суть подхода - вместо того что бы на каждое действия создавать отдельную функцию(ПРЕДСТАВЛЕНИЕ), то
    мы имеем возможность обьеденить их в один класс.
    В данном примере мы выводим весь список(list()) и получим конкретный элемент(retrieve())
    ViewSet в urls.py пользует routers, которые нужно зарегистрировать. И  т.к. это набор представлений в одном классе, то
    он сам определяет представления, т.е. урлы, по которым можно достучаться. В данном случае мы определили только list и
    """
    # используем уже созданную модель, что бы получить данные
    queryset = GameModel.objects.filter(id__lt=10)  # возьмем первых 9ть геймеров по их id

    def list(self, request):
        """с помошью serializer определяем вид ответа(как в форме), нашего queryset"""
        serializer = GameModelSerializer(self.queryset, many=True)  # передаем наши данные в форму(сериалайзер) что бы придать \
        # заданного вида нашим данным и т.к. это list, то разрешаем выводим множество записей сразу
        return Response(serializer.data)  # и возвращаем наши уже готовые данные

    def retrieve(self, request, pk=None):
        """
        прикол в том что если клиент захочет получит какой-то конкретный обьект, то pk сам передастся в ссылке:
        lesson_10_drf_2/ ^view-set-example/(?P<pk>[^/.]+)/$ [name='gamemodel-detail']
        """
        user = get_object_or_404(self.queryset, pk=pk)  # пытаемся из уже полученного queryset взять нашу запись(обьект)
        serializer = GameModelSerializer(user)  # вид вывода только имя и почта
        return Response(serializer.data)


print('~~~ 4.) Пример реализации представления Generic + CRUD(l) ~~~~')
class MyCreateGenericAPIView(CreateAPIView):
    """позволять по урл(представлению) создавать новых геймеров. Просто создавать данные."""
    serializer_class = GameModelSerializer  # и все!! CreateAPIView определить какую модель использует сиреалайзер и какие поля \
    # для инпута подставлять в представлении


class MyRetrieveGenericAPIView(RetrieveAPIView):
    queryset = GamerModel.objects.all()  # для отображения, нужно указать элементы в которых мы будем искать ОДИН  нужный нам
    serializer_class = GamerModelSerializer  # ну и вид отображения и модель RetrieveAPIView сам определить через сериалайзер


class MyRetrieveUpdateGenericAPIView(RetrieveUpdateAPIView):
    # таким же образом просто определяем список эелементов в которых мы будем искать нужный нам + благодаря \
    # RetrieveUpdateAPIView добавилась возможность еще и изменять запись
    queryset = GamerModel.objects.all()
    serializer_class = GamerModelSerializer


