from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    return render(request, 'app/search.html', {"searched":searched, "keys":keys})
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    context = {'form': form}
    return render(request,'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'user or password not correct!')

    context = {}
    return render(request,'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request,'app/home.html', context)

    # if request.user.is_authenticated:
    #     customer = request.user
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitems_set.all()
    #     cartItem = order.get_cart_items
    # else:
    #     items = []
    #     order = {'get_cart_items': 0, 'get_cart_total': 0}
    #     cartItem = order['get_cart_items']
    #
    # product = Product.objects.all()
    # context = {'products': product, 'cart': cartItem}
    # return render(request, 'home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitems_set.all()
    else:
        items = [],
        order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order}
    return render(request,'app/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitems_set.all()
    else:
        items = [],
        order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order}
    return render(request,'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItems, created = OrderItems.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItems.quantity +=1
    elif action == 'remove':
        orderItems.quantity -=1
    orderItems.save()
    if orderItems <=0:
        orderItems.delete()

    return JsonResponse('added',safe=False)
















