from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from .forms import IdentifyForm
from .models import (UserModel,
                     Product,ProductCategory,ProductItem,
                     ProductVariation,SizeCategory,SizeOption,
                     Color,Brand,OrderItem,Order,Address,Payment)
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib import messages
from django.views import View
from django.views.generic.base import TemplateView

# Create your views here.

class SampleView(TemplateView):
    template_name = 'sample.html'




class RegisterView(View):
    def get(self, request):
        fm = RegisterForm()
        context = {
            'form' : fm
        }
        return render(request, 'authentication/register.html', context)
    def post(self, request):
        fm = RegisterForm(data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.add_message(request,messages.SUCCESS,'Account created successfully')
            return redirect('signin')
        return redirect('home')


class SigninView(View):

    def get(self, request):
        fm = LoginForm()
        context = {
        'form' : fm
        }
        return render(request, 'authentication/signin.html', context)
    
    def post(self, request):
        fm = LoginForm(data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_authenticated:
                    login(request, user)
                    messages.add_message(request,messages.SUCCESS,'Logged in as '+username)
                    
                    next = request.GET.get('next',None)
                    if next:
                        return redirect(next)
                    return redirect('home')
        messages.add_message(request,messages.ERROR,'Invalid username or password')
        return redirect('signin')




#function based view
# def home(request):  
#     return render(request, 'index.html')


#class based view
class HomeView(View):
    def get(self, request):
        # context = {
        #     'products' : ProductItem.objects.all()
        # }
        return render(request, 'index.html')

class ProductView(View):
    def get(self, request,slug):
        productitem =ProductItem.objects.get(slug=slug)
        sizeoptions = ProductVariation.objects.filter(ProductItem=productitem)
        context = {
            'product' : productitem,
            'sizeoptions' : sizeoptions
        }
        return render(request, 'product.html',context)
    
class SelectsizeView(View):
    def get(self, request, sizename,slug):
        productitem =ProductItem.objects.get(slug=slug)
        sizeoptions = ProductVariation.objects.filter(ProductItem=productitem)
        context = {
            'product' : productitem,
            'sizeoptions' : sizeoptions,
            'sizename' : sizename
        }
        return render(request,'product.html', context)
    


def cart(request):
    cartitems = OrderItem.objects.filter(user=request.user,ordered=False).order_by('-id')
    totalitems = cartitems.count()
    totalprice = 0
    totalsalprice=0
    totalamtsaved = 0
    for item in cartitems:
        totalsalprice += item.get_total_discount_productitem_price()
        totalprice += item.get_total_productitem_price()
        totalamtsaved += item.get_amount_saved()
    context = {
        'cartitems': cartitems,
        'totalitems': totalitems,
        'totalamtsaved': totalamtsaved,
        'totalprice': totalprice,
        'totalsalprice': totalsalprice
    }
    return render(request, 'cart1.html', context)


@login_required
def add_to_cart(request, slug,size,category):
    productitem = ProductItem.objects.get(slug=slug)
    if OrderItem.objects.filter(productitem=productitem,ordered=False).exists():
        orderitem = OrderItem.objects.get(productitem=productitem,ordered=False)
        orderitem.quantity += 1
        orderitem.save()
    else:
        user = UserModel.objects.get(username=request.user)
        sizecategory = SizeCategory.objects.get(category_name=category)
        sizeoption = SizeOption.objects.get(size_name__contains=size,
                                            size_category=sizecategory)
        OrderItem.objects.create(user=user, productitem=productitem,
                                 size=sizeoption,ordered=False)
        messages.add_message(request,messages.SUCCESS,'one item added to cart')
    return redirect('cart')

def increment_quantity(request,id):
    item = OrderItem.objects.get(id=id)
    item_qty = ProductVariation.objects.get(ProductItem=item.productitem,sizeOption=item.size)
    if item_qty.qty_in_stock > item.quantity:
        item.increment_quantity()
        messages.add_message(request,messages.SUCCESS,'item quantity incremented')
    else:
        messages.add_message(request,messages.ERROR,'item out of stock')
    return redirect('cart')

def decrement_quantity(request,id):
    item = OrderItem.objects.get(id=id)
    item.decrement_quantity()
    messages.add_message(request,messages.ERROR,'item quantity decremented')
    return redirect('cart')

def remove_orderitem(request,id):
    item = OrderItem.objects.get(id=id)
    item.delete()
    messages.add_message(request,messages.ERROR,'one item removed from cart')
    return redirect('cart')




# template based view

# class HomeView(TemplateView):
#     template_name = 'index.html'


class SignoutView(View):

    def get(self, request):
        logout(request)
        messages.add_message(request,messages.SUCCESS,'Loggedout')
        return redirect('home')

class ForgotPasswordView(View):
    def get(self, request):
        context = {
        'form' : IdentifyForm()
        }
        return render(request, 'authentication/identify.html',context)
    
    def post(self,request):
        fm = IdentifyForm(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            if UserModel.objects.filter(email=email).exists():
                username = UserModel.objects.get(email=email).username
                encode = urlsafe_base64_encode(force_bytes(username))
                return redirect('/reset_password/'+encode)
            return redirect('signin')

class ResetPasswordView(View):

    def get(self, request,username):
        username = force_str(urlsafe_base64_decode(username))
        user = UserModel.objects.get(username=username)
        context = {
        'form' : SetPasswordForm(user=user)
        }
        return render(request,'authentication/resetpwd.html',context)
    
    def post(self,request,username):
        username = force_str(urlsafe_base64_decode(username))
        user = UserModel.objects.get(username =username )
        fm = SetPasswordForm(data=request.POST,user = user)
        if fm.is_valid():
            fm.save()
            return redirect('signin')
        return redirect('home')



#payment

from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class PaymentView(View):
    def get(self, request):
        return render(request, 'payments/payment.html', {
            'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY
        })

    def post(self, request):
        amount = 5000  
        try:
            charge = stripe.Charge.create(
                    amount=amount,
                    currency='inr',
                    description='Charge Description',
                    source=request.POST['stripeToken']
            )
            return render(request, 'payments/success.html')
        except stripe.error.StripeError:
            return render(request, 'payments/error.html')
        

class OrdersView(View):
    def get(self, request):
        user = UserModel.objects.get(username=request.user)
        orders = Order.objects.filter(user=user,ordered=True).order_by('-id')
        context = {'orders': orders}
        return render(request, 'orders.html', context)

from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class Pymentview(View):
    def get(self,request):
        return render(request,'payments/payment.html',{
            'stripe_public_key':settings.STRIPE_TEST_PUBLIC_KEY
        })
    def post(self,request):
        orderitems=Order.objects.filter(user=request.user,ordered=False)
        totalsalprice = 0
        for item in orderitems:
            totalsalprice += item.items.get_total_discount_productitem_price()

        
        try:
            charge = stripe.Charge.create(
                amount=totalsalprice*100,
                currency = 'inr',
                description = 'charge Discription',
                source = request.POST['stripeToken']
            )
            user = UserModel.objects.get(username=request.user)
            payment=Payment.objects.create(stripe_charge_id=charge['id'],
                                            user=user,
                                            amount=totalsalprice)
            
            orderitems.update(ordered=True,payment=payment)

            return render(request,'payments/success.html')
        except stripe.error.StripeError:
            return render (request,'payments/error.html')
        

# checkout

from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm,CouponForm
from django.utils import timezone

def is_valid_form(values):
    valid = True
    for field in values:
        if field=='':
            valid = False
    return valid

class Checkoutview(View):
    def get(self,request):
        user = UserModel.objects.get(username=request.user)
        cartitems = OrderItem.objects.filter(user=user,ordered=False)
       
        for item in cartitems:
            Order.objects.create(user=user,ordered=False,items=item,ordered_date=timezone.now())
        cartitems.update(ordered=True)

        context = {
            'checkoutform':CheckoutForm(),
            'coupon':CouponForm()
        }
        return render(request,'payments/checkout.html',context)
    
    def post(self,request,args,*kwargs):
        form = CheckoutForm(self.request.POST)
        user = UserModel.objects.get(username=request.user)
        try:
            order = Order.objects.filter(user=user,ordered=False)[0]
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')

                if use_default_shipping:

                    address_qs = Address.objects.filter(
                        User=self.request.user,
                        address_type = 'S',
                        default = True
                    )
                    if address_qs.exists():
                        shipping_address=address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.add_message(messages.INFO,"No default shipping address available")
                        return redirect("checkout")

                else:
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_counrty = form.cleaned_data.get('shipping_country')
                    shipping_pincode = form.cleaned_data.get('shipping_pincode')

                    if is_valid_form([shipping_address1,shipping_counrty,shipping_pincode]):
                        shipping_address = Address(
                            user = self.request.user,
                            street_address = shipping_address1,
                            apartment_address = shipping_address2,
                            country = shipping_counrty,
                            zip = shipping_pincode,
                            address_type = 'S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.add_message(messages.INFO, "Please fill in the required shipping address fields")
                
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type='B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    address_qs = Address.objects.filter(
                        user = self.request.user,
                        address_type = 'B',
                        default = True
                    )
                    if address_qs.exists():
                        billing_address= address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available"
                        )
                        return redirect("checkout")
                else:
                    print("user is entering a new billing address")
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_pincode = form.cleaned_data.get('billing_pincode')

                    if is_valid_form([billing_address1,billing_country,billing_pincode]):
                        billing_address = Address(
                            user = self.request.user,
                            street_address= billing_address1,
                            apartment_address =billing_address2,
                            country=billing_country,
                            zip=billing_country,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default=True
                            billing_address.save()

                    else:
                        messages.add_message(messages.INFO,"please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                return redirect('payment')

        except ObjectDoesNotExist:
            messages.add_message(messages.warning, "you do not have an active order")
            return redirect("cart")
        
#helloworld