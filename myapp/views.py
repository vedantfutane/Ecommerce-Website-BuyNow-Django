from django import forms
from django.conf import settings
from django.db.models import Count,Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponse, JsonResponse
import razorpay
from requests import request
from . models import Cart, Customer, OrderPlaced, Product,Payment
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,"myapp/home.html")

def upcoming(request):
    return render(request,"myapp/upcoming.html")

def about(request):
    return render(request,"myapp/about.html")

def contact(request):
    return render(request,"myapp/contact.html")



class ShopView(View):
    def get(self,request,val):
        product= Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,"myapp/shop.html",locals())
    

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,"myapp/customerregistration.html",locals())
    
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congrats Regestration Done Successfully")
        else:
            messages.warning(request,"Invalid Data Input")
        return render(request,"myapp/customerregistration.html",locals())
    
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,"myapp/profile.html",locals())
        
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congrats! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,"myapp/profile.html",locals())
    
def address(request):
    add =Customer.objects.filter(user=request.user)
    return render(request,"myapp/address.html",locals())

class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,"myapp/updateaddress.html",locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congrats! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
    

    
    
def add_to_cart(request):
    user=request.user
    prod_id=request.GET.get('product_id')
    product=Product.objects.get(id=prod_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount=amount+value
    totalamount=amount+70
    return render(request,"myapp/addtocart.html",locals())


class checkout (View):
    def get(self, request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity* p.product.discounted_price
            famount=famount + value
        totalamount = famount + 70
        razoramount = int(totalamount*100)
        
    
class checkout (View):
    def get(self, request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity* p.product.discounted_price
            famount=famount + value
        totalamount = famount + 70
        razoramount = int(totalamount*100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data={"amount":razoramount,"currency":"INR","receipt":"order_receipt_11"}
        payment_response=client.order.create(data=data)
        print(payment_response)
        #{'id': 'order_MI0T8Od3NF1G0i', 'entity': 'order', 'amount': 546700, 'amount_paid': 0, 'amount_due': 546700, 'currency': 'INR', 'receipt': 'order_receipt_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1690282080}
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status=='created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'myapp/checkout.html',locals())


def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id') 
    cust_id=request.GET.get('cust_id')
    
    #print("payment_done : oid = ",order_id," pid = ",payment_id," cid=",cust_id)
    user=request.user
    #return redirect("orders")
    customer=Customer.objects.get(id=cust_id)
    #To update payment status and payment id
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id    
    payment.save()
    #To save order details
    #"OrderPlaced" is not defined Pylance(reportUndefinedVariable) 
    
    cart=Cart.objects.filter(user=user)
    for p in cart:
        OrderPlaced(user=user, customer=customer, product=p.product, quantity=p.quantity,payment=payment).save() 
        p.delete()
        
    return redirect("orders")



def plus_cart(request):
    if request.method=='GET':
        product_id=request.GET['product_id']
        c= Cart.objects.get(Q(product=product_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
        totalamount=amount+70
        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount   
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method=='GET':
        product_id=request.GET['product_id']
        c= Cart.objects.get(Q(product=product_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
        totalamount=amount+70
        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount   
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method=='GET':
        product_id=request.GET['product_id']
        c= Cart.objects.get(Q(product=product_id)& Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
        totalamount=amount+70
        
        data={
            'amount':amount,
            'totalamount':totalamount   
        }
        return JsonResponse(data)
    
    
