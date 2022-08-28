from django.contrib.auth.models import User
import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
import json
import datetime
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
# Create your views here.
from cart.cartserializer import UserinSerializer, FoodCourtSerializer, FoodResturantSerializer, OrderSerializer, \
    OrderProductsSerializer, BranchMenuSerializer, AllMainOrdersSerializer, AllRestOrdersSerializer, RateSerializer
from cart.models import CostumerProfile, Orders, OrderProducts
from menu.models import BranchMenu, BranchesMenusItems
from restrant.models import CourtsBranches, FoodCourt, RestaurantBranches, BranchesProfile, RestaurantProfile


@api_view(['POST'])
def userReg(request):
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone = request.POST.get('phone')
    city = request.POST.get('city')
    obj, create = User.objects.get_or_create(username=email, first_name=first_name, last_name=last_name, email=email)
    CostumerProfile.objects.get_or_create(name=obj, phone=phone, city=city, )
    token = Token.objects.get(user=obj.id)
    name = obj.get_full_name()
    data = {"key": token.key,
            "name": name}
    json_stuff = UserinSerializer(data).data
    return Response(json_stuff)


@api_view(['POST'])
def userLogn(request):
    email = request.POST.get('email')
    try:
        obj = User.objects.get(username=email)
        token = Token.objects.get(user=obj.id)
        name = obj.get_full_name()
        data = {"key": token.key,
                "name": name}
        json_stuff = UserinSerializer(data).data
        return Response(json_stuff)
    except:
        return Response('No Account with this Email')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def get_Rate(request):
    get_rest = CostumerProfile.objects.get(name=request.user)
    get_or = Orders.objects.filter(name=get_rest, is_rate=False, status='COMPLETE').first()
    if get_or is not None:
        data = {
            "rest": get_or.restaurant.trade_name,
            "id": get_or.id,
        }
        order_data = RateSerializer(data).data
        return Response(order_data)
    return Response('none')

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def get_OrdrStut(request):
    get_rest = CostumerProfile.objects.get(name=request.user)
    get_or = Orders.objects.filter(name=get_rest,status__in=['COMPLETE','PROCESS'])
    data ={}
    if get_or:
        data = OrderSerializer(get_or,many=True).data
    return Response(data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def addRate(request):
    get_id = request.POST.get('order_id')
    get_rate = request.POST.get('rate')
    get_or = Orders.objects.get(id=get_id, )
    get_or.is_rate = True
    get_or.rate = get_rate
    get_or.save()
    return Response('done')

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def sndodrrcved(request):
    get_id = request.POST.get('order')
    get_or = Orders.objects.get(id=get_id, )
    get_or.status = 'RECIEVED'
    get_or.save()
    return Response('done')


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def get_Code(request):
    language = request.headers['Accept-language']
    code = request.POST.get('code')
    section = request.POST.get('section')
    get_rest = CostumerProfile.objects.get(name=request.user)
    get_or = Orders.objects.filter(name=get_rest, status='CREATED')
    for i in get_or:
        i.status = 'LOST'
        i.save()
    if section == 'court':
        obj = CourtsBranches.objects.get(code=code)
        instance = FoodCourt.objects.filter(court=obj)
        data = {}
        if instance:
            data = FoodCourtSerializer(instance, many=True, context={'lang': language}).data
        return Response(data)
    if section == 'restaurant':
        obj = RestaurantBranches.objects.get(table_code=code)
        get_rest = CostumerProfile.objects.get(name=request.user)
        Orders.objects.create(name=get_rest, restaurant=obj.restaurant, branch=obj.branch, table_no=obj.table_no,
                              status='CREATED')
        instance = BranchMenu.objects.filter(branch=obj.branch)
        data = {}
        if instance:
            data = FoodResturantSerializer(instance, many=True, context={'lang': language}).data
        return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def courtSubMenu(request):
    get_rest = CostumerProfile.objects.get(name=request.user)
    language = request.headers['Accept-language']
    sub = request.query_params.get('section')

    get_brh = BranchesProfile.objects.get(id=sub)
    Orders.objects.create(name=get_rest, restaurant=get_brh.restaurant, branch=get_brh, status='CREATED')
    instance = BranchMenu.objects.filter(branch=get_brh)
    data = {}
    if instance:
        data = FoodResturantSerializer(instance,many=True, context={'lang': language}).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getResturantSubMenu(request):
    language = request.headers['Accept-language']
    sub = request.query_params.get('section')
    obj = BranchMenu.objects.get(id=sub)
    instance = BranchesMenusItems.objects.filter(branch_menu=obj, avalb=True)
    data = BranchMenuSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def api_cart(request):
    language = request.headers['Accept-language']
    get_us = CostumerProfile.objects.get(name=request.user)
    # try:
    order = Orders.objects.get(name=get_us, status='CREATED')

    instance = order.orderproducts_set.all()
    data = OrderProductsSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)
    # except:
    #     return Response('No item Purchased')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def api_cartTotal(request):
    get_us = CostumerProfile.objects.get(name=request.user)
    # try:
    order = Orders.objects.get(name=get_us, status='CREATED')
    order_data = OrderSerializer(order).data
    return Response(order_data)

    # except:
    #     return Response('No item Purchased')


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiCartActionProduct(request):
    get_us = CostumerProfile.objects.get(name=request.user)
    productID = request.POST.get('item_id')
    order = Orders.objects.get(name=get_us, status='CREATED')
    get_product = BranchesMenusItems.objects.get(id=productID)
    get_price = get_product.menu.price
    orderitem, ordercreated = OrderProducts.objects.get_or_create(order=order, menu=get_product
                                                                  , price=get_price)

    orderitem.quantity = (orderitem.quantity + 1)
    orderitem.save()

    return JsonResponse('Item Add', safe=False)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiCartAction(request):
    productID = request.POST.get('item_id')
    action = request.POST.get('action')
    if action == 'add':
        get_OrderProduct = OrderProducts.objects.get(id=productID)
        get_OrderProduct.quantity = (get_OrderProduct.quantity + 1)
        get_OrderProduct.save()
        return JsonResponse('Item Add', safe=False)
    elif action == 'remove':
        orderitem = OrderProducts.objects.get(id=productID)
        orderitem.quantity = (orderitem.quantity - 1)
        orderitem.save()
        if orderitem.quantity <= 0:
            orderitem.delete()
        return JsonResponse('Item Removed', safe=False)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiAddNote(request):
    get_us = CostumerProfile.objects.get(name=request.user)
    note = request.POST.get('new_note')
    created = Orders.objects.get(name=get_us, status='CREATED')
    created.note = note
    created.save()
    return Response('Note Added ')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def cancelOrder(request):
    get_us = CostumerProfile.objects.get(name=request.user)

    get_order = Orders.objects.get(name=get_us, status='CREATED')
    get_order.status = 'CANCELLED'
    get_order.save()
    return JsonResponse('Order Cancelled', safe=False)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def makePaymentCash(request):
    get_ur = CostumerProfile.objects.get(name=request.user)
    order = Orders.objects.get(name=get_ur, status='CREATED')
    order.payment_sys = 'Cash On Counter'
    order.status = 'PAID'
    order.save()
    return Response('Done')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def makePayment(request):
    get_ur = CostumerProfile.objects.get(name=request.user)
    order = Orders.objects.get(name=get_ur, status='CREATED')
    get_trdr = RestaurantProfile.objects.get(id=order.branch.restaurant.id)
    if get_trdr.trader_payment:
        url = 'https://api.test.paymennt.com/mer/v2.0/checkout/web'
        data = {
            "requestId": str(order.transaction_id) + "ORDID{}".format(order.id),
            "orderId": str(order.transaction_id),
            "currency": "AED",
            "amount": float(order.get_cart_total),

            "items": [
                {
                    "name": "Dark grey sunglasses",
                    "unitprice": 50,
                    "quantity": 2,
                    "linetotal": 100
                }
            ],
            "customer": {
                "firstName": get_ur.name.first_name,
                "lastName": get_ur.name.last_name,
                "email": get_ur.name.email,
                "phone": get_ur.phone
            },
            "billingAddress": {
                "name": get_ur.name.get_full_name(),
                "address1": get_ur.city,
                "city": get_ur.city,
                "country": "AE"
            },

            "returnUrl": "https://c1fa-154-180-127-87.ngrok.io/cart/paymrespone/",

            "defaultPaymentMethod": "CARD",
            "language": "EN"
        }

        r = requests.post(url, headers={
            "X-PointCheckout-Api-Key": get_trdr.payment_profile_id,
            "X-PointCheckout-Api-Secret": get_trdr.payment_aut,
            "content-type": 'application/json'
        }, data=json.dumps(data),
                          )
        x = r.json()
        return HttpResponse(x['result']['redirectUrl'])
    else:
        return HttpResponse('http://www.menu-less.com/cashierpayment.html')


@api_view(['GET'])
def paymrespone(request):
    tran_ref = request.GET.get('reference')
    chekout_ref = request.GET.get('checkout')
    x = tran_ref.split("ORDID", 1)[1]
    y = tran_ref.split("ORDID", 1)[0]
    order = Orders.objects.get(id=x, transaction_id=y, status='CREATED')
    order.tran_ref = chekout_ref
    order.payment_result = 'Paid'
    order.status = 'PAID'
    order.save()
    return HttpResponse(status=200)


# Resturant

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiMainOrders(request):
    language = request.headers['Accept-language']
    get_farm = BranchesProfile.objects.get(user=request.user)
    instance = Orders.objects.filter(branch=get_farm, status__in=['PAID', 'PROCESS','COMPLETE'])
    data = {}
    if instance:
        data = AllMainOrdersSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiSubOrders(request):
    language = request.headers['Accept-language']
    order_id = request.POST.get('order_id')
    obj = Orders.objects.get(id=order_id)
    instance = OrderProducts.objects.filter(order=obj)
    data = {}
    if instance:
        data = AllMainOrdersSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiMainOrdersAction(request):
    dataid = request.POST.get('ordrid')
    action = request.POST.get('action')
    instance = Orders.objects.get(id=dataid)
    instance.status = action
    instance.save()
    return Response('done')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiRestMainOrders(request):
    language = request.headers['Accept-language']
    get_rest = RestaurantProfile.objects.get(name=request.user)

    instance = Orders.objects.filter(restaurant=get_rest, status__in=['PAID','PROCESS','COMPLETE']).order_by('-id')[:20]
    data = {}
    if instance:
        data = AllRestOrdersSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def apiBrhLstOrders(request):
    language = request.headers['Accept-language']
    get_rest = BranchesProfile.objects.get(user=request.user)

    instance = Orders.objects.filter(branch=get_rest, status__in=['COMPLETE', 'PROCESS','DELIVERED']).order_by('-id')[:10]
    data = {}
    if instance:
        data = AllRestOrdersSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def qrcodefind(request):
    dataid = request.POST.get('ordrid')

    instance = Orders.objects.get(transaction_id=dataid)
    data= {}
    if instance:
        data = AllMainOrdersSerializer(instance).data
    return Response(data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def ordrfind(request):
    dataid = request.POST.get('ordrid')
    instance = Orders.objects.get(transaction_id=dataid)
    data= {}
    if instance:
        data = AllMainOrdersSerializer(instance).data
    return Response(data)