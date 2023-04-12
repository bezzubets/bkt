from django.contrib import admin
from .models import Category, Art, Product, Season, Size, Brand, Color, People, Socks, Wear, SocksList, \
    WearsList, Customer, Postoffice, Number_Office, Cities, DeliveryAddress, Cart, CartProduct, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city',
                    'name_post_office',
                    'num_post_office', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]





admin.site.register(People)
admin.site.register(Art)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Season)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Socks)
admin.site.register(Wear)
admin.site.register(SocksList)
admin.site.register(WearsList)
admin.site.register(Customer)
admin.site.register(Postoffice)
admin.site.register(Number_Office)
admin.site.register(Cities)
admin.site.register(DeliveryAddress)
admin.site.register(Cart)
admin.site.register(CartProduct)


