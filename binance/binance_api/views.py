import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Crypto, Favorite_crypto
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def get_all_tickers(request):
    """Выполняется это если была нажата кнопка вывода списка крипты
    Если в бд не заполнена, то заполняет её всем что есть на бинансе
    Если бд заполнена, то обновляет всю бд"""

    context = Crypto().get_all_tickers()
    return render(request, 'crypto_list.html', {'cryptos': context})


def get_one_ticket(request):
    """Выполняется это если была нажата кнопка поиска конкретной крипты"""
    
    context = Crypto().get_one_ticket(request.POST.get("input_submit"))
    return render(request, 'crypto_list.html', {'cryptos': context})


@login_required
def add_to_favorite(request):
    pk_list = request.POST.getlist('checkbox')
    favorite_objects = Crypto.objects.filter(pk__in=pk_list)
    for favor in favorite_objects:
        Favorite_crypto.objects.update_or_create(
            crypto=favor, user=request.user)

    context = Favorite_crypto.objects.filter(user=request.user)
    return render(request, 'favorite_list.html', {'favorite_crypto': context, 'pk_list': pk_list})


@login_required
def check_favorite_list(request):

    context = Favorite_crypto.objects.filter(user=request.user)
    return render(request, 'favorite_list.html', {'favorite_crypto': context})


@login_required
def delete_to_favorite(request):
    pass


@login_required
def favorite_list(request):

    context = Favorite_crypto.objects.all()
    return render(request, 'favorite_list.html', {'cryptos': [{'favorite_crypto': context}]})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправляем на главную страницу после авторизации
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def layout(request):
    if request.method == "POST":

        if request.POST.get("btn_submit_ticket"):
            return get_one_ticket(request)

        elif request.POST.get("btn_submit_all"):
            return get_all_tickers(request)

        elif request.POST.get("btn_add_favorite"):
            return redirect('favorite_list')
            # return add_to_favorite(request)

        elif request.POST.get("btn_check_favorite_list"):
            return check_favorite_list(request)

        elif request.POST.get("btn_change_user") or request.POST.get("btn_login_out"):
            return redirect('/login')

        return render(request, 'crypto_list.html', {'cryptos': cryptos})
    return render(request, 'crypto_list.html', {'cryptos': [{'symbol': 'Введите название криптовалюты'}]})
