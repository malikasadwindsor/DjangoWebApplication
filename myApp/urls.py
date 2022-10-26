from django.urls import path
from myApp import views

app_name = 'myApp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'detail/<int:cat_no>', views.detail, name='detail')
    ]
