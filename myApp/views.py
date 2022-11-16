#import libraries
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm


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


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myApp/products.html', {'prodlist': prodlist})

def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product']
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                product = Product.objects.get(name=product_name)
                product.stock = product.stock - order.num_units
                product.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order !!!'
                return render(request, 'myApp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myApp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})

def productdetail(request, prod_id):
    try:
        msg = ''
        product = Product.objects.get(id=prod_id)
        # product = get_object_or_404(Product, pk=prod_id)
        if request.method == 'GET':
            form = InterestForm()
        elif request.method == 'POST':
            form = InterestForm(request.POST)
            if form.is_valid():
                interested = form.cleaned_data['interested']
                print("Interested: ", interested)
                if int(interested) == 1:
                    product.interested += 1
                    product.save()
                    print('form is valid')
                    return redirect(reverse('myApp:index'))
        # else:
        #     form = InterestForm()
        return render(request, 'myApp/productdetail.html', {'form': form, 'msg': msg, 'product': product})
    except Product.DoesNotExist:
        msg = 'The requested product does not exist. Please provide correct product id !!!'
        return render(request, 'myApp/productdetail.html', {'msg': msg})