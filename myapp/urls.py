from django.conf import settings
from django.urls import path, include
from myapp import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

app_name = 'myapp'

urlpatterns = [
    path(r'home', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'', views.index, name='index'),
    path(r'logged', views.user_login, name='login'),
    path(r'register', views.register, name='register'),
    path(r'<int:cat_no>', views.detail, name='detail'),
    path(r'products', views.products, name='products'),
    path(r'products/<int:prod_id>', views.productdetail, name='product_detail'),
    path(r'placeorder', views.place_order, name='place_order'),
    path(r'myorders', views.my_orders, name='my_order'),
    # path(r'logout', views.logout, name='logout'),
    path(r'logout/', LogoutView.as_view(next_page='myapp:index'), name='logout'),
    path(r'forgot', views.forgot_password, name='forgot')
]
