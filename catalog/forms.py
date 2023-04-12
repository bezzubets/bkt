from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Order, Cities, Postoffice, Number_Office, Category, Brand, Season, Size, Color
from django.forms import ModelForm, TextInput, EmailInput, Select


class ChoiceForm(forms.Form):
    category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Выберите категорию',
                                      queryset=Category.objects.all(), required=False,
                                      widget=forms.Select(attrs={"class": "form-control"}))
    brand = forms.ModelChoiceField(empty_label='Выберите бренд', label='Выберите бренд',
                                   queryset=Brand.objects.all(), required=False,
                                   widget=forms.Select(attrs={"class": "form-control"}))
    season = forms.ModelChoiceField(empty_label='Выберите сезон', label='Выберите сезон',
                                    queryset=Season.objects.all(), required=False,
                                    widget=forms.Select(attrs={"class": "form-control"}))
    size = forms.ModelChoiceField(empty_label='Выберите размер', label='Выберите размер',
                                  queryset=Size.objects.all(), required=False,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    color = forms.ModelChoiceField(empty_label='Выберите цвет', label='Выберите цвет',
                                   queryset=Color.objects.all(), required=False,
                                   widget=forms.Select(attrs={"class": "form-control"}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Имя пользователя', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ph_number = forms.CharField(label='Номер телефона(опционально)', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', required=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', required=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'ph_number')


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'name_post_office',
                  'num_post_office']
        widgets = {
            'first_name': TextInput(attrs={"class": "form-control", }),
            'last_name': TextInput(attrs={"class": "form-control", }),
            'email': EmailInput(attrs={"class": "form-control", }),
            'phone': TextInput(attrs={"class": "form-control", }),
            'address': TextInput(attrs={"class": "form-control", }),
            'postal_code': TextInput(attrs={"class": "form-control", }),
            'city': Select(choices=Cities.objects.all(), attrs={"class": "form-control", }),
            'name_post_office': Select(choices=Postoffice.objects.all(), attrs={"class": "form-control", }),
            'num_post_office': Select(choices=Number_Office.objects.all(), attrs={"class": "form-control", })

        }
