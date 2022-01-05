from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from store.models import customer, product
from .models import Product
from .models import Category
from .models import Customer
from .models import Order
# Create your views here.
def index(request):
    if request.method=="GET":
        
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}
        products=None
        categories=Category.get_all_products()
        catid=request.GET.get('category')
        if catid:
            products=Product.get_all_products_by_id(catid)
        else:
            products=Product.get_all_products()
        data={}
        data['products']=products
        data['categories']=categories
        return render(request,'index.html',data)
    else:
        product=request.POST.get('product')
        cart=request.session.get('cart')
        remove=request.POST.get('remove')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity==1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        return redirect('homepage')


def signup(request):
    if request.method=="GET":
        return render(request,'signup.html')
    else:
        fname=request.POST.get('Name')
        username=request.POST.get('Username')
        emailid=request.POST.get('EmailId')
        password=request.POST.get('Password')
        password=make_password(password)
        customer=Customer(name=fname,uname=username,email=emailid,pwd=password)
        isExists=customer.isExists()
        if isExists:
            return HttpResponse("Email Already Exists")
        else:
            customer.register()
            return redirect('homepage')

def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        username=request.POST.get('Username')
        password=request.POST.get('Password')
        customer=Customer.get_customer_by_username(username)
        request.session['customer_id']=customer.id
        if customer:
            flag=check_password(password,customer.pwd)
            if flag:
                request.session['customer_id']=customer.id
                request.session['customer_name']=customer.uname
                return redirect('homepage')
            else:
                return HttpResponse("Invalid EmailId or Password")
        else:
            return HttpResponse("Invalid EmailId or Password")
        return render(request,'login.html')

def cart(request):
    ids=list(request.session.get('cart').keys())
    products=Product.get_all_products_by_id(ids)
    return render(request,'cart.html',{'products':products})

def checkout(request):
    addr=request.POST.get('address')
    phone=request.POST.get('phone')
    customer=request.session.get('customer_id')
    print("customer",customer)
    cart=request.session.get('cart')
    ids=list(request.session.get('cart').keys())
    products=Product.get_all_products_by_id(ids)
    for product in products:
        order=Order(customer=Customer(id=customer),product=product,price=product.price,quantity=cart.get(str(product.id)),
                    address=addr,phone=phone)
        order.placeOrder()
    request.session['cart']={}
    return redirect('cart')

def orders(request):
    customer = request.session.get('customer_id')
    orders = Order.get_orders_by_customer(customer)
    print(orders)
    return render(request , 'orders.html'  , {'orders' : orders})

def logout(request):
    request.session.clear()
    return redirect('login')