"""ilearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as authViews
urlpatterns = [
    # rest
    path('apiRestMainOrders/', views.apiRestMainOrders, name="apiRestMainOrders"),
    # brnh
    path('apiMainOrders/', views.apiMainOrders, name="apiMainOrders"),
    path('apiMainOrdersAction/', views.apiMainOrdersAction, name="apiMainOrdersAction"),
    path('apiBrhLstOrders/', views.apiBrhLstOrders, name="apiBrhLstOrders"),
    path('qrcodefind/', views.qrcodefind, name="qrcodefind"),
    path('ordrfind/', views.ordrfind, name="ordrfind"),
    # user
    path('userReg/', views.userReg, name="userReg"),
    path('userLogn/', views.userLogn, name="userLogn"),
    path('get_Code/', views.get_Code, name="get_Code"),
    path('getResturantSubMenu/', views.getResturantSubMenu, name="getResturantSubMenu"),
    path('apiCartActionProduct/', views.apiCartActionProduct, name="apiCartActionProduct"),
    path('courtSubMenu/', views.courtSubMenu, name="courtSubMenu"),
    path('api_cart/', views.api_cart, name="api_cart"),
    path('apiCartAction/', views.apiCartAction, name="apiCartAction"),
    path('api_cartTotal/', views.api_cartTotal, name="api_cartTotal"),
    path('makePaymentCash/', views.makePaymentCash, name="makePaymentCash"),
    path('apiAddNote/', views.apiAddNote, name="apiAddNote"),
    path('makePayment/', views.makePayment, name="makePayment"),
    path('cancelOrder/', views.cancelOrder, name="cancelOrder"),
    path('addRate/', views.addRate, name="addRate"),
    path('get_Rate/', views.get_Rate, name="get_Rate"),
    path('get_OrdrStut/', views.get_OrdrStut, name="get_OrdrStut"),
    path('sndodrrcved/', views.sndodrrcved, name="sndodrrcved"),



]
