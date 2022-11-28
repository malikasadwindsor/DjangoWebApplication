from django.contrib import admin
from django.contrib import admin
from .models import Product, Category, Client, Order

# admin.site.register(Product)
admin.site.register(Category)


# admin.site.register(Client)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'client', 'num_units', 'order_status_choices', 'order_status', 'status_date', 'order_total')


admin.site.register(Order, OrderAdmin)


@admin.action(description='Update Stock')
def update_stock(self, request, queryset):
    for q in queryset:
        q.stock += 50
        q.save()


# Question 1
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'stock', 'available')
    actions = [update_stock]


admin.site.register(Product, ProductAdmin)


# Question 2
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'city', 'get_interest')


admin.site.register(Client, ClientAdmin)
