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
    path('getCategory/', views.getCategory, name="getCategory"),
    path('getsectionCategory/', views.getsectionCategory, name="getsectionCategory"),
    path('addMenuCategory/', views.addMenuCategory, name="addMenuCategory"),
    path('addMenuItems/', views.addMenuItems, name="addMenuItems"),
    path('getRestCategory/', views.getRestCategory, name="getRestCategory"),
    path('removeRestCategory/', views.removeRestCategory, name="removeRestCategory"),
    path('detailRestCategory/', views.detailRestCategory, name="detailRestCategory"),
    path('removeMenuItem/', views.removeMenuItem, name="removeMenuItem"),
    path('getbrnhList/', views.getbrnhList, name="getbrnhList"),
    path('getBranchCategory/', views.getBranchCategory, name="getBranchCategory"),
    path('clearBranchCategory/', views.clearBranchCategory, name="clearBranchCategory"),
    # branch
    path('getBrchCategory/', views.getBrchCategory, name="getBrchCategory"),
    path('detailBrchCategory/', views.detailBrchCategory, name="detailBrchCategory"),
    path('deactiveBrhItem/', views.deactiveBrhItem, name="deactiveBrhItem"),


]
