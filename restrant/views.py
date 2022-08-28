import uuid
from django.contrib.auth.models import User
import decimal
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

#### user
from restrant.forms import CreateUser
from restrant.models import *
from restrant.restserializer import LogininSerializer, BranchesSerializer, CourtTablesSerializer, \
    BranchesTablesSerializer, CourtDataSerializer, PlanSerializer, RegDataSerializer


@api_view(['GET'])
def getCryRate(request):
    sub = request.query_params.get('cry')
    obj = CountryCode.objects.get(countrycode=sub)
    url = 'https://api.exchangerate.host/convert?from=USD&to=' + obj.currency
    response = requests.get(url)
    data = response.json()

    get_rate = decimal.Decimal(data['info']['rate'])
    data = {"go": round(obj.go_pln * get_rate,2),
            "start": round(obj.strt_pln * get_rate,2),
            "elite": round(obj.elit_pln * get_rate,2),
            "symbl": obj.currency,
            }

    json_stuff = PlanSerializer(data).data
    return Response(json_stuff)


@api_view(['POST'])
def createRest(request):
    plan = request.POST.get('plan')
    city = request.POST.get('city')
    email = request.POST.get('email')
    password = request.POST.get('password')
    fname = request.POST.get('fname')
    country = request.POST.get('country')
    lname = request.POST.get('lname')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    trade_name = request.POST.get('trade')
    logo = request.FILES.get('logo')
    obj = CountryCode.objects.get(countrycode=country)
    data = {
        'first_name': fname,
        'last_name': lname,
        'email': email,
        'username': email,
        'password1': password,
        'password2': password,
    }
    form = CreateUser(data)

    if form.is_valid():
        user = form.save()
        name = RestaurantProfile.objects.create(name=user, phone=phone, address=address,
                                                trade_name=trade_name, logo=logo, city=city,
                                                country=obj.country)
        url = 'https://api.exchangerate.host/convert?from=USD&to=' + obj.currency
        response = requests.get(url)
        data = response.json()
        transaction = datetime.datetime.now().timestamp()
        if plan == 'go':
            price = obj.go_pln
            period = obj.go_period
            get_rate = decimal.Decimal(data['info']['rate'])
            rat = round(get_rate * price, 2)
            totl = round((get_rate * price) * (period), 2)
            g_totl = round(price * period, 2)
            ord = SubscriptionOrders.objects.create(name=name, price=price, total=g_totl, c_total=totl, rate=get_rate,
                                                    symbol=obj.currency,transaction_id = transaction,
                                                    period=period)
            data2 = {"rate": rat,
                     "key": ord.id,
                     "name": name.trade_name,
                     "symbl": obj.currency,
                     "period": period,
                     "total": totl,
                     "logo": name.logo.url}
            json_stuff = RegDataSerializer(data2).data
            return Response(json_stuff)
        elif plan == 'start':
            price = obj.strt_pln
            period = obj.strt_period
            get_rate = decimal.Decimal(data['info']['rate'])
            rat = round(get_rate * price, 2)
            totl = round((get_rate * price) * (period), 2)
            g_totl = round(price * period, 2)
            ord = SubscriptionOrders.objects.create(name=name, price=price, total=g_totl, c_total=totl, rate=get_rate,
                                                    symbol=obj.currency,transaction_id = transaction,
                                                    period=period)
            data2 = {"rate": rat,
                     "key": ord.id,
                     "name": name.trade_name,
                     "symbl": obj.currency,
                     "period": period,
                     "total": totl,
                     "logo": name.logo.url}
            json_stuff = RegDataSerializer(data2).data
            return Response(json_stuff)
        elif plan == 'elite':
            price = obj.elit_pln
            period = obj.elit_period
            get_rate = decimal.Decimal(data['info']['rate'])
            rat = round(get_rate*price,2)
            totl = round((get_rate*price)*(period),2)
            g_totl = round(price*period,2)
            ord = SubscriptionOrders.objects.create(name=name, price=price,total=g_totl,c_total=totl,rate=get_rate
                                                    ,symbol=obj.currency,transaction_id = transaction,
                                                    period=period)
            data2 = {"rate": rat,
                    "okey": ord.id,
                    "name": name.trade_name,
                    "symbl": obj.currency,
                    "period": period,
                    "total": totl,
                    "logo": name.logo.url}
            json_stuff = RegDataSerializer(data2).data
            return Response(json_stuff)
    else:
        return JsonResponse(form.errors)

@api_view(['POST'])
def restPayment(request):
    key = request.POST.get('key')

    order = SubscriptionOrders.objects.get(id=key)

    url = 'https://api.test.paymennt.com/mer/v2.0/checkout/web'
    data = {
        "requestId": str(order.transaction_id)+ "ORDID{}".format(order.id) ,
        "orderId": str(order.transaction_id),
        "currency": "AED",
        "amount": float(order.c_total),

        "items": [
            {
                "name": "Dark grey sunglasses",
                "unitprice": 50,
                "quantity": 2,
                "linetotal": 100
            }
        ],
        "customer": {
            "firstName": order.name.name.first_name,
            "lastName": order.name.name.last_name,
            "email": order.name.name.email,
            "phone": order.name.phone
        },
        "billingAddress": {
            "name": order.name.name.get_full_name(),
            "address1": order.name.city,
            "city": order.name.city,
            "country": "AE"
        },

        "returnUrl": "https://c1fa-154-180-127-87.ngrok.io/cart/paymrespone/",

        "defaultPaymentMethod": "CARD",
        "language": "EN"
    }

    r = requests.post(url, headers={
        "X-PointCheckout-Api-Key": "1823b1a512e0ee78",
        "X-PointCheckout-Api-Secret": "mer_83ab2060c73bf5a955eaf9bb93c1f0db1db1baaed7c417aa3b5f33c446674b92",
        "content-type": 'application/json'
    }, data=json.dumps(data),
                      )
    x = r.json()
    return HttpResponse(x['result']['redirectUrl'])


@api_view(['GET'])
def restPaymrespone(request):
    tran_ref = request.GET.get('reference')
    chekout_ref = request.GET.get('checkout')
    x = tran_ref.split("ORDID", 1)[1]
    y = tran_ref.split("ORDID", 1)[0]

    order = SubscriptionOrders.objects.get(id=x, transaction_id=y, status='CREATED')
    today = datetime.datetime.now().date()
    get_date = order.period * 30
    new_date = today + datetime.timedelta(get_date)
    order.tran_ref = chekout_ref
    order.status = 'PAID'
    order.until_date = new_date
    order.save()
    obj = RestaurantProfile.object.get(subscriptionorders=order)
    obj.approve = True
    obj.until_date = new_date
    obj.save()

    return Response("done")



@api_view(['POST'])
def loginRest(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        get_user = User.objects.get(username=user)
        token, create = Token.objects.get_or_create(user=get_user)
        try:
            name = RestaurantProfile.objects.get(name=get_user)
            if name.approve:
                key = token.key
                data = {"key": key,
                        "name": name.trade_name,
                        "logo": name.logo.url
                        }
                json_stuff = LogininSerializer(data).data
                return Response(json_stuff)
            else:
                ord = SubscriptionOrders.objects.get(name=name, status='CREATED')
                rat = round(ord.rate * ord.price, 2)

                data2 = {"rate": rat,
                         "okey": ord.id,
                         "name": name.trade_name,
                         "symbl": ord.symbol,
                         "period": ord.period,
                         "total": ord.c_total,
                         "logo": name.logo.url}
                json_stuff = RegDataSerializer(data2).data
                return Response(json_stuff)
        except:
            return JsonResponse('Wrong Password or Email', safe=False)
    else:
        return JsonResponse('Wrong Password or Email', safe=False)

@api_view(['POST'])
def loginbrch(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        get_user = User.objects.get(username=user)
        token, create = Token.objects.get_or_create(user=get_user)
        try:
            name = BranchesProfile.objects.get(user=get_user)
            key = token.key
            data = {"key": key,
                    "name": name.restaurant.trade_name,
                    "logo": name.restaurant.logo.url
                    }
            json_stuff = LogininSerializer(data).data
            return Response(json_stuff)
        except:
            return JsonResponse('Wrong Password or Email', safe=False)
    else:
        return JsonResponse('Wrong Password or Email', safe=False)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def createBranch(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    name = request.POST.get('name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    data = {
        'username': username,
        'password1': password,
        'password2': password,
    }
    form = CreateUser(data)
    if form.is_valid():
        user = form.save()
        obj = BranchesProfile.objects.create(restaurant=get_rest, name=name, user=user)

        return Response(obj.id)
    else:
        return JsonResponse(form.errors, safe=False)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def createTables(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    branch = request.POST.get('branch')
    get_brh = BranchesProfile.objects.get(id=branch)
    table_no = int(request.POST.get('table_no'))

    for i in range(table_no):
        lst = i + 1
        code = uuid.uuid4().hex
        RestaurantBranches.objects.create(restaurant=get_rest, branch=get_brh, table_no=lst, table_code=code)
    return Response('Done')


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def createCourtBranch(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    branch = request.POST.get('branch')
    court = request.POST.get('court')
    get_brh = BranchesProfile.objects.get(id=branch)
    get_crt = CourtsBranches.objects.get(id=court)
    FoodCourt.objects.create(restaurant=get_rest, branch=get_brh, court=get_crt)
    return Response('Done')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getBranchs(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    instance = BranchesProfile.objects.filter(restaurant=get_rest)
    data = {}
    if instance:
        data = BranchesSerializer(instance, many=True, ).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getTablesBranchs(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    sub = request.query_params.get('branch')
    obj = BranchesProfile.objects.get(id=sub)
    instance = RestaurantBranches.objects.filter(branch=obj)
    data = {}
    if instance:
        data = BranchesTablesSerializer(instance, many=True, ).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getFoodCourt(request):
    instance = CourtsBranches.objects.all()
    data = {}
    if instance:
        data = CourtTablesSerializer(instance, many=True, ).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getCourtBrnh(request):
    sub = request.query_params.get('branch')
    obj = BranchesProfile.objects.get(id=sub)
    instance = FoodCourt.objects.get(branch=obj)
    data = {}
    if instance:
        data = CourtDataSerializer(instance).data
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def removetBrnh(request):
    sub = request.query_params.get('branch')
    BranchesProfile.objects.get(id=sub).delete()

    return Response('done')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getRestPymt(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    data = {
        "tax": get_rest.tax,
        "vat": get_rest.vat,
        "service": get_rest.service,
    }
    return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getcrtyPyGat(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    get_crty = CountryCode.objects.get(country=get_rest.country)
    data = {
        "paybtn": get_crty.pyment,

    }
    return Response(data)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getReststg(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    data = {
        "profile": get_rest.payment_profile_id,
        "auth": get_rest.payment_aut,
    }
    return Response(data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def sendRestPymt(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    tax = request.POST.get('tax')
    vat = request.POST.get('vat')
    service = request.POST.get('service')
    get_rest.tax = tax
    get_rest.vat = vat
    get_rest.service = service
    get_rest.save()
    return Response('done')


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def updatRestPymt(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    profile = request.POST.get('profile')
    auth = request.POST.get('auth')
    get_rest.trader_payment = True
    get_rest.payment_profile_id = profile
    get_rest.payment_aut = auth
    get_rest.save()
    return Response('Update done')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getBrnhFees(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    instance = BranchesProfile.objects.filter(restaurant=get_rest)
    data = {}
    if instance:
        data = BranchesSerializer(instance, many=True, ).data
    return Response(data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def updBrnhFees(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    branch = request.POST.get('branch')
    instance = BranchesProfile.objects.get(id=branch)
    instance.srv = True
    instance.service = get_rest.service
    instance.save()

    return Response('Done')


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def rmvBrnhFees(request):
    branch = request.POST.get('branch')
    instance = BranchesProfile.objects.get(id=branch)
    instance.srv = False
    instance.service = 0.0
    instance.save()

    return Response('Done')


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def printingBrh(request):
    get_rest = BranchesProfile.objects.get(user=request.user)
    if get_rest.is_branch:
        instance = RestaurantBranches.objects.filter(branch=get_rest)
        data = {}
        if instance:
            data = BranchesTablesSerializer(instance, many=True, ).data
        return Response(data)
    else:
        instance = FoodCourt.objects.filter(branch=get_rest)
        data = {}
        if instance:
            data = CourtDataSerializer(instance, many=True, ).data
        return Response(data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def printingRest(request):
    sub = request.query_params.get('branch')
    get_rest = BranchesProfile.objects.get(id=sub)
    if get_rest.is_branch:
        instance = RestaurantBranches.objects.filter(branch=get_rest)
        data = {}
        if instance:
            data = BranchesTablesSerializer(instance, many=True, ).data
        return Response(data)
    else:
        instance = FoodCourt.objects.filter(branch=get_rest)
        data = {}
        if instance:
            data = CourtDataSerializer(instance, many=True, ).data
        return Response(data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def rstSndSprt(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    sub = request.POST.get('sub')
    qset = request.POST.get('qset')
    ResSupport.objects.create(restaurant=get_rest, subj=sub, question=qset)
    return Response('Done')


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def brhSndSprt(request):
    get_rest = BranchesProfile.objects.get(user=request.user)
    sub = request.POST.get('sub')
    qset = request.POST.get('qset')
    ResSupport.objects.create(branch=get_rest, subj=sub, question=qset)
    return Response('Done')
