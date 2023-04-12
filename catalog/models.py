from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class People(models.Model):
    people = models.CharField(max_length=20, help_text='Люди.Для кого товар.')

    def __str__(self):
        return self.people


class Art(models.Model):
    art = models.CharField(max_length=20, help_text='Артикул')

    def __str__(self):
        return self.art


class Category(models.Model):
    category = models.CharField(max_length=20, help_text='Категория товара', verbose_name='Категория товара')

    def __str__(self):
        return self.category


class Brand(models.Model):
    brand = models.CharField(max_length=50, help_text='Бренд', verbose_name='Бренд')

    def __str__(self):
        return self.brand


class Season(models.Model):
    season = models.CharField(max_length=20, help_text='Наименование сезона', verbose_name='Наименование сезона')

    def __str__(self):
        return self.season


class Size(models.Model):
    size = models.CharField(max_length=20, help_text='Размер', verbose_name='Размер')

    def __str__(self):
        return self.size


class Color(models.Model):
    color = models.CharField(max_length=20, help_text='Цвет', verbose_name='Цвет')

    def __str__(self):
        return self.color


class SocksList(models.Model):
    sockslist = models.CharField(max_length=20, help_text='Виды носков', verbose_name='Виды носков')

    def __str__(self):
        return self.sockslist


class WearsList(models.Model):
    wearslist = models.CharField(max_length=20, help_text='Виды одежды', verbose_name='Виды одежды')

    def __str__(self):
        return self.wearslist


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Postoffice(models.Model):
    name_post = models.CharField(max_length=100, help_text='Название перевозчика',
                                 verbose_name='Название перевозчика', blank=True)

    def __str__(self):
        return self.name_post


class Number_Office(models.Model):
    number_office = models.CharField(max_length=10, help_text='Номер отделения',
                                     verbose_name='Номер отделения', blank=True)

    def __str__(self):
        return self.number_office


class Cities(models.Model):
    cities = models.CharField(max_length=20, help_text='Город',
                              verbose_name='Город', blank=True)

    def __str__(self):
        return self.cities


class DeliveryAddress(models.Model):
    lastname = models.CharField(max_length=20, help_text='Фамилия', verbose_name='Фамилия', blank=True)
    firstname = models.CharField(max_length=20, help_text='Имя', verbose_name='Имя', blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, help_text='Название организации',
                                 verbose_name='Название организации', blank=True, null=True)
    phone = models.CharField(max_length=14, help_text='Номер телефона', verbose_name='Номер телефона', blank=True)
    cities = models.ForeignKey(Cities, on_delete=models.CASCADE, help_text='Город',
                               verbose_name='Город', blank=True, null=True)
    postoffice = models.ForeignKey(Postoffice, on_delete=models.CASCADE, help_text='Название перевозчика',
                                   verbose_name='Название перевозчика', blank=True, null=True)
    numberoffice = models.ForeignKey(Number_Office, on_delete=models.CASCADE, help_text='Номер отделения',
                                     verbose_name='Номер отделения', blank=True, null=True)
    deliveryaddress = models.CharField(max_length=50, help_text='Улица, проспект, переулок',
                                       verbose_name='Улица, проспект, переулок', blank=True)
    number = models.CharField(max_length=5, help_text='Номер дома', verbose_name='Номер дома', blank=True)
    apt = models.CharField(max_length=5, help_text='Номер квартиры (если есть)',
                           verbose_name='Номер квартиры (если есть)', blank=True)
    index = models.CharField(max_length=20, help_text='Почтовый индекс', verbose_name='Почтовый индекс',
                             blank=True, null=True)
    desc = models.TextField(help_text='Комментарии к заказу', verbose_name='Комментарии к заказу', blank=True)

    def __str__(self):
        return self.deliveryaddress


class Product(models.Model):
    people = models.ManyToManyField(People, help_text='Люди. Для кого товар', verbose_name='Кому товар предназначен')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Категория товара',
                                 verbose_name='Категория товара')
    wearlist = models.ForeignKey(WearsList, on_delete=models.CASCADE, help_text='Вид одежды',
                                 verbose_name='Вид одежды', blank=True, null=True)
    socklist = models.ForeignKey(SocksList, on_delete=models.CASCADE, help_text='Вид носков',
                                 verbose_name='Вид носков', blank=True, null=True)
    art = models.ForeignKey(Art, on_delete=models.PROTECT, help_text='Артикул', verbose_name='Артикул', blank=True)
    title = models.CharField(max_length=50, help_text='Наименование', verbose_name='Наименование', blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, help_text='Бренд', verbose_name='Бренд')
    season = models.ManyToManyField(Season, help_text='Наименование сезона',
                                    verbose_name='Наименование сезона')
    price = models.CharField(max_length=10, help_text='Цена', verbose_name='Цена', blank=True)
    size = models.ManyToManyField(Size, help_text='Размер изделия', verbose_name='Размер изделия')
    pic = models.ImageField(upload_to='static/photo/%Y/%m/%d/', db_index=True,
                            verbose_name='Фото', blank=True)
    color = models.ManyToManyField(Color, help_text='Цвет', verbose_name='Цвет')
    components = models.CharField(max_length=250, help_text='Состав изделия', verbose_name='Состав изделия', blank=True)
    description = models.TextField(help_text='Описание товара', verbose_name='Описание товара', blank=True)
    add_product = models.CharField(max_length=20, help_text='Количество товара',
                                   verbose_name='Добавить количество товара',
                                   blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})


class Wear(Product):
    def __str__(self):
        return self.title


class Socks(models.Model):
    def __str__(self):
        return self.title


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.CharField(max_length=10, help_text='Цена', verbose_name='Цена', blank=True)

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.products.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.CharField(max_length=10, help_text='Цена', verbose_name='Цена', blank=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField()
    phone = models.CharField(max_length=13, verbose_name='Телефон', null=True)
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name='Город')
    name_post_office = models.ForeignKey(Postoffice, on_delete=models.CASCADE, verbose_name='Перевозчик', null=True)
    num_post_office = models.ForeignKey(Number_Office, on_delete=models.CASCADE, verbose_name='Номер отделения',
                                        null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
