from django.urls import path
from . import views

urlpatterns = [
    path('search', views.layout, name='layout'),
    path('favorite_list', views.favorite_list, name='favorite_list'),
    path('login/', views.login_view, name='login_view')
]

