from datetime import datetime

from django import forms
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import OrderForm, InterestForm, UserLogin, RegisterForm, ForgotPassword
from .models import Category, Product, Client, Order
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User


# Create your views here.
# def detail(request, cat_no):
#     category = get_object_or_404(Category, id=cat_no)
#     prod_list = Product.objects.filter(category__id=cat_no).order_by('id')
#     response = HttpResponse()
#     text = '<p>' + 'Warehouse Location: ' + str(category) + '</p>'
#     response.write(text)
#     text = '<p>' + 'List of products: ' + '</p>'
#     response.write(text)
#     for product in prod_list:
#         text = '<p>' + str(product.id) + ': ' + str(product) + ' ' + str(product.price) + '</p>'
#         response.write(text)
#     return response


def index(request):
    if request.user.username != '':
        request.session.set_expiry(3600)
        cat_list = Category.objects.all().order_by('id')[:10]
        msg = ''

        if 'last_login' not in request.session:
            request.session['last_login'] = User.objects.get(username=request.user.username). \
                last_login.strftime('%y-%m-%d %a %H:%M:%S')
            msg = '<span class="text-custom-two fw-bold">Last Login: </span> More than one hour ago'
        else:
            msg = '<span class="text-custom-two fw-bold">Last Login: </span>' + request.session['last_login']
    # return render(request, 'myapp/index0.html', {'cat_list': cat_list}) commented out as requested in lab 6, part 3
    else:
        cat_list = Category.objects.all().order_by('id')[:10]
        msg = ''

    return render(request, 'myapp/index.html', {'msg': msg, 'cat_list': cat_list, 'user': request.user})


def about(request):
    msg = ''
    request.session.set_expiry(300)

    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 0
    msg = request.session['about_visits']
    return render(request, 'myapp/about.html', {'msg': msg})

    # response = HttpResponse()
    # text = '<p>' + 'This is an Online Store APP.' + '</p>'
    # response.write(text)
    # return response


def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    prod_list = Product.objects.filter(category__id=cat_no).order_by('id')
    return render(request, 'myapp/detail.html', {'prod_list': prod_list, 'category': category})

    # response = HttpResponse()
    # text = '<p>' + 'Warehouse Location: ' + str(category) + '</p>'
    # response.write(text)
    # text = '<p>' + 'List of products: ' + '</p>'
    # response.write(text)
    # for product in prod_list:
    #    text = '<p>' + str(product.id) + ': ' + str(product) + ' ' + str(product.price) + '</p>'
    #    response.write(text)
    # return response


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prod_list = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units < order.product.stock:
                order.product.stock -= order.num_units
                order.product.save()
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prod_list': prod_list})


def productdetail(request, prod_id):
    prod = Product.objects.filter(id=prod_id).get()
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == '1':
                prod.interested += 1
            prod.save()
            return HttpResponseRedirect('/myapp/')
    else:
        form = InterestForm()
    return render(request, 'myapp/product_detail.html', {'form': form, 'prod': prod})


def user_login(request):
    form_class = UserLogin
    form = form_class(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                user_obj = User.objects.get(username=username)
                num = request.session.get('login')
                if num is not None:
                    request.session['login'] = 0
                    return HttpResponseRedirect(reverse('myapp:my_order'))
                else:
                    return HttpResponseRedirect(reverse('myapp:index'), {'user': user_obj})
                # return HttpResponseRedirect(reverse('myapp:myorders', {'username': username))
                # return render(request, 'myapp/index.html', {'user': user_obj})
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


def my_orders(request):
    msg = ''
    order_list = []
    if request.user.username == '':
        request.session['login'] = 1
        user_login(request)
        form_class = UserLogin
        form = form_class(request.POST)
        return render(request, 'myapp/login.html', {'form': form})
    else:
        if Client.objects.filter(username=request.user.username).exists():
            if Order.objects.filter(client__username=request.user.username).exists():
                order_list = Order.objects.filter(client__username=request.user.username)
                msg = 'User Found'
            else:
                msg = 'You currently have no orders.'
        else:
            msg = 'You are not a registered client.'
        return render(request, 'myapp/myorders.html', {'msg': msg, 'order': order_list})


def register(request):
    form_class = RegisterForm
    if request.FILES:
        form = form_class(request.POST, request.FILES)
    else:
        form = form_class(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('myapp:login'))
        else:
            return render(request, 'myapp/register.html', {'form': form, 'msg': 'Form is incorrect'})
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


def forgot_password(request):
    user = ''
    form = ForgotPassword(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        if Client.objects.filter(username=username).exists():
            user = Client.objects.get(username=username)
            password = Client.objects.make_random_password(length=10)
            user.set_password(password)
            user.save()
            msg = 'Your password has been changed. Your new Password is: ' + password
            status = send_mail('Password Changed', msg, None, [user.email], fail_silently=False)
            response_msg = ''
            if status == 1:
                response_msg = 'New password is sent to your registered email.'
            else:
                response_msg = 'Password sending failed!'
            return render(request, 'myapp/forgot_password_response.html',
                          {'msg': response_msg})
    else:
        return render(request, 'myapp/forgot_password.html', {'form': form})
    return render(request, 'myapp/forgot_password_response.html', {'msg': 'Invalid username'})
