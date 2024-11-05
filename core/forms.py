from django import forms
from .models import UserModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    gender = forms.ChoiceField(widget=forms.RadioSelect(),choices=[['male','MALE'],['female','FEMALE']])
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email','gender', 'username',
                  'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(
        attrs={
            'type': 'password',
        }
    ))

class IdentifyForm(forms.Form):
    email = forms.CharField(max_length=30)

PAYMENT_CHOICES = ( ('S','stripe'),('R','Razorpay'))
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required = False,
        widget = CountrySelectWidget(attrs={
            'class':'custom-select d-block w-100',
        }))
    shipping_pincode =forms.CharField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)

    same_billing_address = forms.BooleanField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label = '(select country)').formfield(
        required=False,
        widget = CountrySelectWidget(attrs={
            'class':'custom_select d-block w-100',
        }))
    billing_pincode = forms.CharField(required=False)

    
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices = PAYMENT_CHOICES)
 


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder' : 'Promo code'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4
    }))
    email = forms.EmailField()

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)