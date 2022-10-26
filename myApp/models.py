from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return 'Product: Category: '+str(self.category.name)+' Name: '+str(self.name)+ \
               ' Price: '+str(self.price)+\
               ' Stock:'+str(self.stock)+' Availability: '+str(self.available)+\
               ' Description: '+str(self.description)


class Client(User):
    PROVINCE_CHOICES = [('AB', 'Alberta'),
                        ('MB', 'Manitoba'),
                        ('ON', 'Ontario'),
                        ('QC', 'Quebec')]
    company = models.CharField(max_length=50, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return 'Clients:Company: ' + str(self.company) + \
               ' Shipping address: ' + str(self.shipping_address) + ' City:' + str(self.city) + \
               ' Province: ' + str(self.province) +\
               ' Interested in: ' + str(self.interested_in)


class Order(models.Model):
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='clients', on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=100)
    order_status = [(0, 'Order Cancelled'),
                    (1, 'Order Placed'),
                    (2, 'Order Shipped'),
                    (3, 'Order Delivered')]
    orderStatus = models.PositiveIntegerField(max_length=20, choices=order_status, default='--')
    status_date = models.DateField()

    def total_cost(self):
        return self.product.price * self.num_units

    def __str__(self):
        return 'Orders: Product: ' + str(self.product.name) + ' |Client: ' + str(self.client.username) + ' |Num_units: ' \
           + str(self.num_units) + ' |Order Status'+str(self.orderStatus)+ '|Status: ' + str(self.status_date)+' |Total Cost:' +str(Order.total_cost(self))


