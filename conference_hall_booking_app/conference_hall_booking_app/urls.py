"""conference_hall_booking_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from booking.views import AddNewHall, ModifyHall, DeleteHall, show_hall_details, show_all_halls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hall/new/', AddNewHall.as_view(), name='add-new-hall'),
    re_path(r'^hall/modify/(?P<hall_id>\d+)$', ModifyHall.as_view(), name='modify-hall'),
    re_path(r'^hall/delete/(?P<hall_id>\d+)$', DeleteHall.as_view()),
    re_path(r'^hall/(?P<hall_id>\d+)$', show_hall_details),
    re_path(r'^$', show_all_halls, name='home'),
]
