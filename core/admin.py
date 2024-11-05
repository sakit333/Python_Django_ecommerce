from django.contrib import admin
from .models import (UserModel,
                     Product,ProductCategory,ProductItem,
                     ProductVariation,SizeCategory,SizeOption,
                     Color,Brand,OrderItem,
                     Address,Coupon,Payment,Refund,Order)
# Register your models here.
@admin.register(UserModel)
class Usermodeladmin(admin.ModelAdmin):
    list_display = ['mobile_no','address1','address2','dob','gender','picture']


@admin.register(Product)
class ProductModeladmin(admin.ModelAdmin):
    list_display = ['product_id','product_name','product_description','product_category','brand','care_instructions','about','slug']


@admin.register(Color)
class ColorModeladmin(admin.ModelAdmin):
    list_display = ['color_id','color_name' ] 

@admin.register(ProductItem)
class ProductItemModeladmin(admin.ModelAdmin):
    list_display = ['product_item_id','product','color','original_price','sale_price','product_code']

@admin.register(ProductVariation)
class ProductVariationModelAdmin(admin.ModelAdmin):
    list_display = ['VariationId','ProductItem','sizeOption','qty_in_stock']

@admin.register(Brand)
class BrandModeladmin(admin.ModelAdmin):
    list_display = ['brand_id','brand_name','brand_description']

@admin.register(ProductCategory)
class ProductCategoryModeladmin(admin.ModelAdmin):
    list_display = ['product_category_id','category_name','category_description','category_image','size_category']

@admin.register(SizeCategory)
class SizeCategoryModeladmin(admin.ModelAdmin):
    list_display = ['category_id','category_name']

@admin.register(SizeOption)
class SizeOptionModeladmin(admin.ModelAdmin):
    list_display = ['sizeId','size_name','sort_order','size_category']

@admin.register(OrderItem)
class OrderItemModeladmin(admin.ModelAdmin):
    list_display = ['user','ordered','productitem','quantity']

@admin.register(Address)
class AddressItemModeladmin(admin.ModelAdmin):
    list_display = ['user','street_address','apartment_address','country',
                    'zip','address_type','default']
    

@admin.register(Coupon)
class CouponModeladmin(admin.ModelAdmin):
    list_display = ['code','amount']

@admin.register(Payment)
class PaymentModeladmin(admin.ModelAdmin):
    list_display = ['stripe_charge_id','user','amount','timestamp']

@admin.register(Refund)
class RefundModeladmin(admin.ModelAdmin):
    list_display = ['order','reason','accepted','email']

@admin.register(Order)
class OrderModeladmin(admin.ModelAdmin):
    list_display = ['user','ref_code',
                    'items','start_date','ordered_date',
                    'ordered','shipping_address',
                    'billing_address','payment','coupon',
                    'being_delivered','received','refund_requested',
                    'refund_granted']