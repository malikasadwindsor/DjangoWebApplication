from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Category, Product, Client, Order
from django.shortcuts import render

# Create your views here.

def index(request):
      cat_list = Category.objects.all().order_by('id')[:10]
      return render(request, 'myApp/index.html', {'cat_list': cat_list})
    # cat_list = Category.objects.all().order_by('id')[:10]
    # list_of_product = Product.objects.all().order_by('-price')[:5]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of categories: ' + '</p>'
    # response.write(heading1)
    #
    # for category in cat_list:
    #     para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
    #     response.write(para)

    # res_product = HttpResponse()
    # head_2 = '<p>' + 'List of products: ' + '</p>'
    # res_product.write(head_2)
    #
    # for product in list_of_product:
    #     val = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
    #     res_product.write(val)
    # return res_product


def about(request):
    # return HttpResponse("This is an Online Store APP")
    return render(request, 'myApp/about.html')


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    return render(request, 'myApp/detail.html', {'category': category, 'products': products})
    # category = get_object_or_404(Category, pk=cat_no)
    # products = Product.objects.filter(category=category)
    # res_detail = HttpResponse()
    # head = '<p>' + 'Warehouse location - ' + category.warehouse + '</p>'
    # head += '<p>' + 'List of products for the category' + '</p>'
    # res_detail.write(head)
    #
    # for product in products:
    #     val = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
    #     res_detail.write(val)
    # return res_detail