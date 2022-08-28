
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
from django.shortcuts import render

# Create your views here.
from restrant.models import RestaurantProfile, BranchesProfile
from tracking.models import NotifUser, WebContact, OrderTracking, BranchRate
from tracking.trckserializer import NotifSerializer, BranchesRatesSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def notif(request):

    get_notif =NotifUser.objects.filter(name=request.user,is_read=False)
    data ={}
    if get_notif:
        data = NotifSerializer(get_notif,many=True).data
    return Response(data)

@api_view(['POST'])
def webContct(request):
    mail = request.POST.get('mail')
    name = request.POST.get('name')
    msg = request.POST.get('msg')
    WebContact.objects.create(name=mail,mail=name,msg=msg)
    return Response('Done')

# rest
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def dashRates(request):
    get_rest = RestaurantProfile.objects.get(name=request.user)
    instance = BranchRate.objects.filter(restaurant=get_rest)
    data = {}
    if instance:
        data = BranchesRatesSerializer(instance,many=True).data
    return Response(data)