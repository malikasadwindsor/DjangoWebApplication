from django.contrib import admin
from .models import Product, Category, Client, Order
#register models here
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)