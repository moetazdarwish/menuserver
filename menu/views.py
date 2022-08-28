from django.contrib.auth.models import User

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

# Create your views here.
from menu.menuserializer import MenuCategory, MenuRestCategorySerializer, MenuRestItemsSerializer, \
    BranchesListSerializer, MenuBrchCategorySerializer, MenuBrchItemsSerializer
from menu.models import MenusCategory, MenusName, MenusItems, BranchMenu, BranchesMenusItems
from restrant.models import RestaurantProfile, BranchesProfile, RestaurantBranches, FoodCourt
from restrant.restserializer import BranchesTablesSerializer, CourtDataSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getCategory(request):
    language = request.headers['Accept-language']
    instance = MenusCategory.objects.all()
    data = {}
    if instance:
        data = MenuCategory(instance, many=True, context={'lang': language}).data
    return Response(data)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getsectionCategory(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    sub = request.query_params.get('menu')
    language = request.headers['Accept-language']
    instance = MenusCategory.objects.get(id=sub)
    obj ,create = MenusName.objects.get_or_create(restaurant=get_rest, category=instance)
    data = {}
    if instance:
        data = MenuRestCategorySerializer(obj,  context={'lang': language}).data
    return Response(data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def addMenuCategory(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    m_id = request.POST.get('m_id')
    get_m = MenusCategory.objects.get(id=m_id)
    obj = MenusName.objects.get_or_create(restaurant=get_rest, category=get_m)
    return Response(obj.id)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def addMenuItems(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    m_id = request.POST.get('m_id')
    obj = MenusName.objects.get(id=m_id)
    name = request.POST.get('name')
    name_la = request.POST.get('name_la')
    describe = request.POST.get('describe')
    describe_la = request.POST.get('describe_la')
    price = request.POST.get('price')
    photo = request.FILES.get('photo')

    MenusItems.objects.create(menu=obj, category=obj.category, name=name, name_la=name_la, describe=describe,
                              describe_la=describe_la, price=price, photo=photo)
    return Response('Done')

# from rest_framework.pagination import PageNumberPagination
# paginator = PageNumberPagination()
#     paginator.page_size = 2
# result_page = paginator.paginate_queryset(instance, request)
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getRestCategory(request):
    language = request.headers['Accept-language']
    get_rest = RestaurantProfile.objects.get(name=request.user)
    instance = MenusName.objects.filter(restaurant=get_rest)
    data = {}
    if instance:
        data = MenuRestCategorySerializer(instance, many=True, context={'lang': language}).data
    return Response(data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def removeRestCategory(request):
    menu = request.POST.get('menu')
    MenusName.objects.get(id=menu).delete()
    return Response('Done')
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def removeMenuItem(request):
    menu = request.POST.get('menu')
    MenusItems.objects.get(id=menu).delete()
    return Response('Done')

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def detailRestCategory(request):
    language = request.headers['Accept-language']
    menu = request.POST.get('menu')
    obj = MenusName.objects.get(id=menu)
    instance = MenusItems.objects.filter(menu=obj)
    data = {}
    if instance:
        data = MenuRestItemsSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getbrnhList(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    instance = BranchesProfile.objects.filter(restaurant=get_rest)
    data = {}
    if instance:
        data = BranchesListSerializer(instance, many=True, ).data
    return Response(data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getBranchCategory(request):
    data = json.loads(request.body)
    listArray = data['listArray']

    branch = data['branch']
    get_br = BranchesProfile.objects.get(id=branch)
    for i in listArray:
        get_meu = MenusName.objects.get(id=i)
        BranchMenu.objects.get_or_create(branch=get_br, category=get_meu)
    return Response('done')

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def clearBranchCategory(request):
    branch = request.POST.get('branch')
    get_br = BranchesProfile.objects.get(id=branch)
    BranchMenu.objects.filter(branch=get_br).delete()
    return Response('done')

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def getBrchCategory(request):
    language = request.headers['Accept-language']
    get_rest = BranchesProfile.objects.get(user=request.user)
    instance = BranchMenu.objects.filter(branch=get_rest)
    data = {}
    if instance:
        data = MenuBrchCategorySerializer(instance, many=True, context={'lang': language}).data
    return Response(data)
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def detailBrchCategory(request):
    language = request.headers['Accept-language']
    menu = request.POST.get('menu')
    obj = BranchMenu.objects.get(id=menu)
    instance = BranchesMenusItems.objects.filter(branch_menu=obj)
    data = {}
    if instance:
        data = MenuBrchItemsSerializer(instance, many=True, context={'lang': language}).data
    return Response(data)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def deactiveBrhItem(request):
    menu = request.POST.get('menu')
    obj = BranchesMenusItems.objects.get(id=menu)
    obj.avalb = not obj.avalb
    obj.save()
    return Response(obj.branch_menu.id)


