from django.contrib import admin
from . models import OrderPlaced, Product
from . models import Customer
from . models import Cart
from . models import Payment

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display= ['id','title','discounted_price','category','product_image']
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display= ['user','name','locality','city','state','mobile','zipcode']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display= ['id','user','product','quantity']
    
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display= ['id','user','amount','razorpay_order_id','razorpay_payment_id','razorpay_payment_status','paid']
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','product','quantity','ordered_date','status','payment']