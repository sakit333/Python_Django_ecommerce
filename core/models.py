from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# Create your models here.

class UserModel(User):
    mobile_no = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address1 = models.CharField(max_length=255,null=True, blank=True)
    address2 = models.CharField(max_length=255,null=True, blank=True)
    gender = models.CharField(max_length=10,choices=[['male','MALE'],['female','FEMALE']])
    picture = models.ImageField(null=True, blank=True,upload_to='profile/')

    
            
class SizeCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
class SizeOption(models.Model):
    sizeId = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=100)
    sort_order = models.CharField(max_length=100)
    size_category = models.ForeignKey(SizeCategory,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return str(self.size_name)

class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100)
    brand_description = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return self.brand_name
    

class ProductCategory(models.Model):
    product_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='category/')
    category_description = models.CharField(max_length=1000)
    size_category = models.ForeignKey(SizeCategory,on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=1000)
    care_instructions = models.CharField(max_length=1000)
    about = models.CharField(max_length=1000)
    slug = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.product_name
    
class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name
    
class ProductItem(models.Model):
    product_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.SET_NULL,null=True)
    original_price = models.IntegerField()
    sale_price = models.IntegerField()
    product_code = models.CharField(max_length=100,null=True, blank=True)
    image1 = models.ImageField(upload_to='product_image/',null=True, blank=True)
    image2 = models.ImageField(upload_to='product_image/',null=True, blank=True)
    image3 = models.ImageField(upload_to='product_image/',null=True, blank=True)
    image4 = models.ImageField(upload_to='product_image/',null=True, blank=True)
    slug = models.CharField(max_length=100,null=True, blank=True)


    def __str__(self):
        return str(self.product_item_id)

    def save(self, *args, **kwargs):
        name = '-'.join(str(self.product).split())
        color = str(self.color)
        brand = str(self.product.brand)
        self.slug = brand+'-'+name+'-'+color
        super().save(*args, **kwargs)

class ProductVariation(models.Model):
    VariationId = models.AutoField(primary_key=True)
    ProductItem = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    sizeOption = models.ForeignKey(SizeOption,on_delete=models.SET_NULL,null=True)
    qty_in_stock = models.IntegerField()

    def __str__(self):
        return str(self.sizeOption)[0]
    
    def size(self):
        s = (self.sizeOption.size_name)[0]
        return s 
    
class OrderItem(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    productitem = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey(SizeOption, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"{self.quantity} of {self.productitem.product}"

    def get_total_productitem_price(self):
        return self.quantity * self.productitem.original_price

    def get_total_discount_productitem_price(self):
        return self.quantity * self.productitem.sale_price

    def get_amount_saved(self):
        return self.get_total_productitem_price() - self.get_total_discount_productitem_price()

    def get_final_price(self):
        if self.productitem.sale_price:
            return self.get_total_discount_productitem_price()
        return self.get_total_productitem_price()

    def increment_quantity(self):
        self.quantity += 1
        self.save()

    def decrement_quantity(self):
        self.quantity -= 1
        self.save()

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

from django_countries.fields import CountryField
class Address(models.Model):
    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(UserModel,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ForeignKey(OrderItem,on_delete=models.CASCADE,null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address,related_name='shipping_address',on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        Address,related_name='billing_address',  on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"