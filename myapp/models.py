from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, default='xyz')

    def __str__(self):
        return self.name


def validate_stock(value):
    if 0 <= value <= 1000:
        return value
    else:
        raise ValidationError("The value is not in the given threshold of the stock parameters")


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[validate_stock])
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        self.stock += 100


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'), ]
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    company = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return self.first_name

    def get_interest(self):
        return ", ".join([i.name for i in self.interested_in.all()])


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=0)
    order_status_choices = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered')]
    order_status = models.PositiveIntegerField(choices=order_status_choices, default=1)
    status_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return 'Product: %s, Client: %s, Units: %s' % (self.product.name, self.client.first_name, self.num_units)

    def printx(self):
        return self.product.price * self.num_units

    @admin.display(description='Order Total')
    def order_total(self):
        return self.product.price * self.num_units
