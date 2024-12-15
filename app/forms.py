"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog
from django import forms
from .models import Tour


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['image', 'country', 'days', 'start_date', 'end_date', 'description', 'price', 'category']  # Добавляем 'category'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'days': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})  # Добавление класса для стилей
        }



from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    passport_exists = forms.ChoiceField(
        choices=[(True, "Да"), (False, "Нет")],
        label="Есть ли у Вас загран паспорт"
    )
    visa_exists = forms.ChoiceField(
        choices=[(True, "Да"), (False, "Нет")],
        label="Есть ли у Вас виза"
    )

    class Meta:
        model = Booking
        fields = ['full_name', 'phone', 'email', 'passport_exists', 'visa_exists']
        labels = {
            'full_name': 'ФИО',
            'phone': 'Номер телефона',
            'email': 'Почта',
        }

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


from django import forms

class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    email = forms.EmailField(label='Ваш email', min_length=7)
    rating_design = forms.IntegerField(label='Оценка дизайна сайта', min_value=1, max_value=10)
    usability = forms.ChoiceField(label='Оценка удобства использования',
                                  choices=(('easy', 'Легко'),
                                           ('medium', 'Средне'),
                                           ('difficult', 'Сложно')))
    improvements = forms.CharField(label='Что можно улучшить на сайте?', widget=forms.Textarea)
    source = forms.ChoiceField(label='Как вы узнали о нашем сайте?',
                               choices=(('search_engine', 'Поисковая система'),
                                        ('social_media', 'Социальные сети'),
                                        ('friend', 'Рекомендация друга'),
                                        ('other', 'Другое')))
    comments = forms.CharField(label='Дополнительные комментарии', widget=forms.Textarea)
    def get_success_url(self):
        return reverse('success_url')

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog # используемая модель
        fields = ('title', 'description', 'content', 'image',) #заполняемые поля
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}

