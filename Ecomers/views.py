from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreation
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def home(request):
    context={}
    return render(request, 'Ecomers/home.html', context)

def main(request):
    product = Product.objects.all()
    data = cartData(request)
    order = data['order']
    items = data['items']
    cart_items = data['cart_items']

    context = {'product': product, 'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'Ecomers/main.html', context)


def cart(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    cart_items = data['cart_items']
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'Ecomers/cart.html', context)


def checkout(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    cart_items = data['cart_items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'Ecomers/checkout.html', context)


def navbar(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_item_total
    else:
        items = []
        order = {'get_cart_total': 0, 'get_item_total': 0, }
        cart_items = 0
    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'Ecomers/navbar.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('productID', productID)
    print('action', action)
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Data is added', safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['userInfo']['Total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shppingInfo']['Address'],
            state=data['shppingInfo']['State'],
            ZipCode=float(data['shppingInfo']['ZipCode']),
            city=data['shppingInfo']['City'],

        )

    return JsonResponse('Payment complete', safe=False)


def registerPage(request):
    form = UserCreation()

    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginPage')

    context = {'form': form}
    return render(request, 'Ecomers/registerPage.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request, username=username, password=password)
        try:
            Customer.objects.create(user=user, name=username)
        except:
            pass
        if user is not None:
            login(request, user)
            return redirect('main')

    context = {}

    return render(request, 'Ecomers/loginPage.html', context)



def logoutPage(request):
    logout(request)
    return redirect('loginPage')
