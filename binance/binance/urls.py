
from django.contrib import admin
from django.urls import path, include
from binance_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.layout), 
    path('', views.layout),
    path('login/', views.login_view, name='login_view')
]