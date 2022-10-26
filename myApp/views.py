from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Category, Product, Client, Order

# Create your views here.

def index(request):
    # cat_list = Category.objects.all().order_by('id')[:10]
    list_of_product = Product.objects.all().order_by('-price')[:5]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of categories: ' + '</p>'
    # response.write(heading1)
    #
    # for category in cat_list:
    #     para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
    #     response.write(para)

    res_product = HttpResponse()
    head_2 = '<p>' + 'List of products: ' + '</p>'
    res_product.write(head_2)

    for product in list_of_product:
        val = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
        res_product.write(val)
    return res_product


def about(request):
    return HttpResponse("E-commerce store")


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    header_response = HttpResponse()
    uri = '<p>' + 'Warehouse location - ' + category.warehouse + '</p>'
    uri += '<p>' + 'List of products for the category' + '</p>'
    header_response.write(uri)

    for product in products:
        val = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
        header_response.write(val)
    return header_response