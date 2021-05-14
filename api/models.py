import datetime
from django.db import models
from auth_.models import Seller, User
from .regions import regions
# Create your models here.


class Region(models.Model):
    region = models.PositiveSmallIntegerField(choices=regions, unique=True)

    def __str__(self):
        return f"{self.region}"


class DeliveryAddress(Region):
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'DeliveryAddress'
        verbose_name_plural = 'DeliveryAddresses'

    def __str__(self):
        return f"{self.region}:{self.address}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Category:{self.name}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductManager(models.Manager):

    def actual(self):
        return self.get_queryset().filter(is_active=True)


class Gadget(models.Model):
    name = models.CharField(max_length=100)
    seller = models.ForeignKey(Seller, on_delete=models.DO_NOTHING, related_name='sel_products', default=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_products')
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0, blank=False)
    amount = models.IntegerField(default=-1)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='gadgets/', blank=True, null=True)

    objects = ProductManager()

    def __str__(self):
        return f"Product: {self.name}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class OrdersManager(models.Manager):

    def create(self, customer, address, total, *args, **kwargs):
        if customer and address:
            order = self.model(customer=customer, delivery_address=address,
                               total=total)
            order.save()
            return order
        else:
            raise ValueError('Some fields are not full')

    def add_product(self, product):
        if product:
            order = self.model
            order.products.add(product)
            order.save()
            return order
        else:
            raise ValueError('Some fields are not full')


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='customer_order')
    total = models.PositiveIntegerField(blank=False)
    products = models.ManyToManyField(Gadget, related_name='order_products', blank=True)
    date = models.DateTimeField( auto_now_add=True, blank=True)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.DO_NOTHING)

    objects = OrdersManager()

    def __str__(self):
        return f"Order: {self.pk}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['date']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Gadget, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    published = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.user} | {self.product}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['published']
