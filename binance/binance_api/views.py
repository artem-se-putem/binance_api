import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Crypto, Favorite_crypto
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def get_all_tickers():
    """Выполняется это если была нажата кнопка вывода списка крипты
    Если в бд не заполнена, то заполняет её всем что есть на бинансе
    Если бд заполнена, то обновляет всю бд"""

    url_name_price = "https://api.binance.com/api/v3/ticker/price"
    url_24hr = "https://data.binance.com/api/v3/ticker/24hr"
    response_name_price = requests.get(url_name_price)
    response_24hr = requests.get(url_24hr)
    if response_name_price.status_code == 200:
        data_name_price = response_name_price.json()
        data_24hr = response_24hr.json()

        lst_all_tickers = []
        # Тут может быть ошибка в data_24hr[index], если в data_24hr элементы расположены в другой порядке чем в data_name_price
        for index, item_name_price in enumerate(data_name_price):
            if data_24hr[index]['symbol'] == item_name_price['symbol']:
                try:
                    crypto_obj = Crypto.objects.get(
                        symbol=item_name_price['symbol'])
                except Crypto.DoesNotExist:
                    Crypto.objects.create(
                        symbol=item_name_price['symbol'],
                        price=item_name_price['price'],
                        change_24h=data_24hr[index]['priceChange'],
                    )
            else:
                Crypto.objects.filter(symbol=crypto_obj.symbol).update(
                    price=item_name_price['price'],
                    change_24h=data_24hr[index]['priceChange'],
                )

        context = Crypto.objects.all()
        return context


def get_one_ticket(symbol=""):
    """Выполняется это если была нажата кнопка поиска конкретной крипты"""

    url_name_price = "https://api.binance.com/api/v3/ticker/price"
    url_24hr = "https://data.binance.com/api/v3/ticker/24hr"
    response_name_price = requests.get(url_name_price)
    response_24hr = requests.get(url_24hr)
    if response_name_price.status_code == 200:
        data_name_price = response_name_price.json()
        data_24hr = response_24hr.json()

        for item_name_price in data_name_price:
            if item_name_price['symbol'] == symbol:
                for item_hr in data_24hr:
                    if item_hr['symbol'] == symbol:
                        item_name_price['priceChange'] = item_hr['priceChange']
                        # Это массив с dict-ами
                        return [item_name_price]
                return [{'symbol': 'Не найдено изменение цены за 24 часа'}]
    return [{'symbol': 'Криптовалюта не найдена в списке бинанса'}]

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
                return redirect('/') # Перенаправляем на главную страницу после авторизации
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def layout(request):
    if request.method == "POST":

        if request.POST.get("btn_submit_ticket"):
            cryptos = get_one_ticket(request.POST.get("input_submit"))

        elif request.POST.get("btn_submit_all"):
            cryptos = get_all_tickers()

        elif request.POST.get("btn_add_favorite"):
            return redirect('favorite_list')
            # return add_to_favorite(request)

        elif request.POST.get("btn_check_favorite_list"):
            return check_favorite_list(request)
        
        elif request.POST.get("btn_change_user") or request.POST.get("btn_login_out"):
            return redirect('/login')

        return render(request, 'crypto_list.html', {'cryptos': cryptos})
    return render(request, 'crypto_list.html', {'cryptos': [{'symbol': 'Введите название криптовалюты'}]})
