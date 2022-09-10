import json
from .models import *


def cookieCart(request):
    try:
        cart_new = json.loads(request.COOKIES['cart_new'])
    except:
        cart_new = {'rayen': 20}

    print('cart_newjson', cart_new)

    print('cart 2 : ', cart_new)

    items = []
    order = {'get_cart_total': 0, 'get_item_total': 0, 'shipping': False}
    cart_items = order['get_item_total']
    for i in cart_new:
        try:
            print('hedhi: ', cart_new)
            cart_items += cart_new[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart_new[i]['quantity'])
            print('total: ', cart_new[i]['quantity'])
            order['get_cart_total'] += total
            order['get_item_total'] += cart_new[i]['quantity']
            print('cartttttttttt:', product.id)

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart_new[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass
    return {'items': items, 'order': order, 'cart_items': cart_items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_item_total

    else:
        cookieData = cookieCart(request)
        cart_items = cookieData['cart_items']
        items = cookieData['items']
        order = cookieData['order']
    return {'items': items, 'order': order, 'cart_items': cart_items}


def guestOrder(request, data):
    print('User is not logged in ...')
    print('COOKIES:', request.COOKIES)
    firstname = data['userInfo']['Firstname']

    email = data['userInfo']['Email']
    cookiedata = cookieCart(request)
    items = cookiedata['items']
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = firstname
    customer.save()
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']

        )

    return customer, order
