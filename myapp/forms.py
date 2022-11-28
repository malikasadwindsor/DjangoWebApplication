from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import TextInput, PasswordInput
from django.forms.utils import ErrorList

from myapp.models import Order, Client


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name'
        }
        widgets = {
            'client': forms.RadioSelect()
        }


class InterestForm(forms.Form):
    CHOICES = [(1, 'YES'), (0, 'NO')]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    quantity = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)


class UserLogin(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={"placeholder": "Username", "type": "text",
                                                       "class": "form-control form-control-user", "id": "id_username"}))
    password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password", "type": "password",
                                                           "class": "form-control form-control-user",
                                                           "id": "id_password"}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'username', 'company', 'interested_in', 'shipping_address',
                  'province', 'city']


class ForgotPassword(forms.Form):
    username = forms.CharField(widget=TextInput(attrs={"placeholder": "Username", "type": "text",
                                                       "class": "form-control form-control-user", "id": "id_username"}))
