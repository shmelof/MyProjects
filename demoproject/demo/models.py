from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils.crypto import get_random_string


def get_file_name(instance, filename):
    return '/'.join(get_random_string(length=5) + '_' + filename)


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь')), default='user')

    USERNAME_FIELD = 'username'

    def full_name(self):
        return ' '.join([self.name, self.patronymic, self.surname])

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Название', blank=False)
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    photo_file = models.ImageField(max_length=254, upload_to=get_file_name,
                                   blank=True, null=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'webp'])
                                    ])
    year = models.IntegerField(verbose_name='Год производства', blank=True)
    country = models.CharField(max_length=254, verbose_name='Страна производства', blank=True)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False, default=0.00)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=1)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Наименование', blank=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False, default=0)

    def __str__(self):
        return self.product.name + ' - ' + str(self.count)


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержденный'),
        ('canceled', 'Отмененный')
    ]
    date = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    status = models.CharField(max_length=254, verbose_name='Статус', choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    rejection_reason = models.TextField(verbose_name='Причина отмены', blank=True)
    products = models.ManyToManyField(Product, through='ItemInOrder', related_name='Orders')

    def count_product(self):
        count = 0
        for item_order in self.iteminorder_set.all():
            count += item_order.count
        return count

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def __str__(self):
        return self.date.ctime() + ' | ' + self.user.full_name() + ' | ' + str(self.count_product())


class ItemInOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', default=0, blank=False)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False, default=0.00)
