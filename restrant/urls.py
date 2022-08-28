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
    path('getCryRate/', views.getCryRate, name="getCryRate"),
    path('createRest/', views.createRest, name="createRest"),
    path('restPayment/', views.restPayment, name="restPayment"),
    path('restPaymrespone/', views.restPaymrespone, name="restPaymrespone"),
    path('loginRest/', views.loginRest, name="loginRest"),
    path('loginbrch/', views.loginbrch, name="loginbrch"),
    path('createBranch/', views.createBranch, name="createBranch"),
    path('createTables/', views.createTables, name="createTables"),
    path('getTablesBranchs/', views.getTablesBranchs, name="getTablesBranchs"),
    path('getFoodCourt/', views.getFoodCourt, name="getFoodCourt"),
    path('getCourtBrnh/', views.getCourtBrnh, name="getCourtBrnh"),
    path('createCourtBranch/', views.createCourtBranch, name="createCourtBranch"),
    path('getBranchs/', views.getBranchs, name="getBranchs"),
    path('removetBrnh/', views.removetBrnh, name="removetBrnh"),
    path('getRestPymt/', views.getRestPymt, name="getRestPymt"),
    path('sendRestPymt/', views.sendRestPymt, name="sendRestPymt"),
    path('getReststg/', views.getReststg, name="getReststg"),
    path('updatRestPymt/', views.updatRestPymt, name="updatRestPymt"),
    path('getBrnhFees/', views.getBrnhFees, name="getBrnhFees"),
    path('updBrnhFees/', views.updBrnhFees, name="updBrnhFees"),
    path('rmvBrnhFees/', views.rmvBrnhFees, name="rmvBrnhFees"),
    path('printingBrh/', views.printingBrh, name="printingBrh"),
    path('printingRest/', views.printingRest, name="printingRest"),
    path('rstSndSprt/', views.rstSndSprt, name="rstSndSprt"),
    path('brhSndSprt/', views.brhSndSprt, name="brhSndSprt"),
    path('getcrtyPyGat/', views.getcrtyPyGat, name="getcrtyPyGat"),


]
