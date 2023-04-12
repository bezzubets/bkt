from django.shortcuts import render, redirect, get_object_or_404
from .models import People, Product, Category, Season, Color, Size, Brand
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, CartAddProductForm, OrderCreateForm, ChoiceForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .filters import ProductFilter
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.views import generic
from .models import OrderItem
from .cart import Cart


def index(request):
    people = People.objects.all()
    products = Product.objects.all()
    context = {
        'people': people,
        'products': products,
    }
    return render(request, 'index.html', context=context)


def catalogue(request):
    data = {}
    filtered_products = ProductFilter(request.GET, queryset=Product.objects.all())
    data['filtered_products'] = filtered_products
    return render(request, 'catalogue.html', data)


class CategoryListView(generic.ListView):
    model = Category
    category = Category.objects.all()
    template_name = 'category_list.html'


def get_category(request, category_id):
    product = Product.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.filter(pk=category_id)
    context = {'category': category, 'categories': categories, 'product': product, }
    return render(request, 'category_list.html', context=context)


class SeasonListView(generic.ListView):
    model = Season
    season = Season.objects.all()
    template_name = 'season_list.html'


def get_season(request, season_id):
    product = Product.objects.all().filter(season=season_id)
    seasons = Season.objects.all()
    season = Season.objects.filter(pk=season_id)
    context = {'season': season, 'seasons': seasons, 'product': product, }
    return render(request, 'season_list.html', context=context)


class ColorListView(generic.ListView):
    model = Color
    color = Color.objects.all()
    template_name = 'color_list.html'


def get_color(request, color_id):
    product = Product.objects.all().filter(color=color_id)
    colors = Color.objects.all()
    color = Color.objects.filter(pk=color_id)
    context = {'color': color, 'colors': colors, 'product': product, }
    return render(request, 'color_list.html', context=context)


class SizeListView(generic.ListView):
    model = Size
    size = Size.objects.all()
    template_name = 'size_list.html'


def get_size(request, size_id):
    product = Product.objects.all().filter(size=size_id)
    sizes = Size.objects.all()
    size = Size.objects.filter(pk=size_id)
    context = {'size': size, 'sizes': sizes, 'product': product, }
    return render(request, 'size_list.html', context=context)


class BrandListView(generic.ListView):
    model = Brand
    brand = Brand.objects.all()
    template_name = 'brand_list.html'


def get_brand(request, brand_id):
    product = Product.objects.all().filter(brand_id=brand_id)
    brands = Brand.objects.all()
    brand = Brand.objects.filter(pk=brand_id)
    context = {'brands': brands, 'brand': brand, 'product': product, }
    return render(request, 'brand_list.html', context=context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = user.email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = 'http://' + domain + link
            user.is_active = False
            email_subject = 'Activate your account'
            email_body = 'Привет ' + user.username + '! С помощью этой ссылки, активируйте свой аккаунт\n' + activate_url
            email = EmailMessage(email_subject, email_body, '______________', [email])
            email.send(fail_silently=False)
            login(request, user)
            messages.success(request, 'Регистрация успешна. На электронную почту мы Вам выслали ссылку для активации. '
                                      'Пожалуйста, перейдите по ней, чтобы активировать Ваш аккаунт.')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = UserRegisterForm(request.POST)
    return render(request, 'register.html', {'form': form})


class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return redirect('index' + '?message=' + 'Пользователь уже активирован.')
            if user.is_active:
                return redirect('index')
            user.is_active = True
            user.save()
            messages.success(request, 'Регистрация успешно активирована')
            return redirect('index')
        except Exception as ex:
            pass
        return redirect('login')


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_product_form = CartAddProductForm()
    return render(request, 'product.html', {'product': product,
                                            'cart_product_form': cart_product_form})


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    return render(request, ('cart/detail.html', {'cart': cart}))


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form})
