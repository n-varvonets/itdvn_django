from django import forms
from durationwidget.widgets import TimeDurationWidget  # pip install django-durationwidget + settings.INSTALLED_APPS указать
from lesson_5.models import Client

# 1) Главной задачей Form - это валидация post данных от клиента. .is_valid() вызывается у экземпляра форм. После проверки \
# можно уже будет обращаться к "чистым данным" по аттрибуту cleaned_data.
# 2) Второстепенной - это нормализация данных. Т.е. приведения конкретного поля к конкретному типу данных тем самым делая её \
# четкую структуру. Подробней смотри презентацию к этому уроку.
# 3) Третей задачей forms - является представление себя в виде html кода(теги и данные). Для этого просто print(forms) экземпляра

# widget - это представления поля формы в виде html

class MyForm(forms.Form):
    """Кастомный вариант формы"""
    name = forms.CharField(label='User name')  # label - меняет название, , disabled=True - отключим данное поле(будет \
    # отображаться, но невозможно ничего ввести)
    email = forms.EmailField(error_messages={'required': 'Input your available email'})  # изменим отображение ошибки required

    # password = forms.PasswordInput() - такая запись в форме не будет отображаться...нужно это поле поместить в виджет:
    password = forms.CharField(
        max_length=20,
        min_length=10,
        widget=forms.PasswordInput()
    )

    # для возможности post работы с файлам
    profile_picture = forms.ImageField(widget=forms.FileInput)
    additional_file = forms.FileField(widget=forms.FileInput)

    age = forms.IntegerField(required=False)
    agreement = forms.BooleanField(required=False, initial=True)
    average_score = forms.FloatField(initial=10.1)  # по дефолту в полю формы выводится эти данные, и если клиент не изменит, \
    # то они пойдут в запрос клиента

    birthday = forms.DateField(widget=forms.SelectDateWidget, required=False,)  # если не указать widget, то будет просто input field
    work_experience = forms.DurationField(required=False,
        widget=TimeDurationWidget(show_hours=False, show_minutes=False, show_seconds=False))  # см. row 2 этого файла
    gender = forms.ChoiceField(choices=[("1", "male"), ("2", "female")], required=False)


class FormModelClient(forms.ModelForm):
    """Наиболее популярный вариант форм, т.к. генерирует нашу форму на лету из
    полей модели и не нужно прописывать кучу всего как в примере выше"""

    class Meta:
        model = Client
        fields = '__all__'  # можно использовать все поля из модели, а можно определенные
        # fields = ['name', 'second_email', 'invoice_doc']