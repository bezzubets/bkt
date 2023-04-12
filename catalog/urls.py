from django.urls import path
from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    url(r'^category_list/$', CategoryListView.as_view(), name='category_list'),
    path('category_list/<int:category_id>/', get_category),
    url(r'^season_list/$', SeasonListView.as_view(), name='season_list'),
    path('season_list/<int:season_id>/', get_season),
    url(r'^color_list/$', ColorListView.as_view(), name='color_list'),
    path('color_list/<int:color_id>/', get_color),
    url(r'^size_list/$', SizeListView.as_view(), name='size_list'),
    path('size_list/<int:size_id>/', get_size),
    url(r'^brand_list/$', BrandListView.as_view(), name='brand_list'),
    path('brand_list/<int:brand_id>/', get_brand),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('product/<int:product_id>/', views.product_detail, name='product'),
    path('cart_detail', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('create/', views.order_create, name='order_create'),
]
