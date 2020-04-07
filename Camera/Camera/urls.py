"""Camera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from blogs import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.register),
    path('addregister',views.addregister),
    path('index',views.index),
    path('done_register',views.done_register),
    path('indext_check',views.indext_check),
    path('select',views.select),
    path('borrow',views.borrow),
    path('Return',views.Return),
    path('test',views.test),
    path('enter',views.enter),
    path('scan',views.scan),
    path('enter_b',views.enter_b),
    path('done_scan',views.done_scan),
    path('done_scan_return',views.done_scan_return),
    path('scan_return',views.scan_return),
    path('complete_borrow',views.complete_borrow),
    path('complete_return',views.complete_return),



    
    
     



]
