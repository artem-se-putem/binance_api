from django.db import models
from django.contrib.auth.models import User
import requests


class Crypto(models.Model):
    symbol = models.CharField(max_length=10, unique=True, default='hey')
    name = models.CharField(max_length=50, default='hey')
    price = models.DecimalField(
        max_digits=20, decimal_places=10, default='100')
    volume = models.DecimalField(
        max_digits=20, decimal_places=10, default='100')
    change_24h = models.DecimalField(
        max_digits=20, decimal_places=10, default='100')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.symbol} ---- {self.price}'

    def _get_all_stats_tickers():
        url_name_price = "https://api.binance.com/api/v3/ticker/price"
        url_24hr = "https://data.binance.com/api/v3/ticker/24hr"
        response_name_price = requests.get(url_name_price)
        response_24hr = requests.get(url_24hr)
        if response_name_price.status_code == 200:
            data_name_price = response_name_price.json()
            data_24hr = response_24hr.json()
            return data_name_price, data_24hr

    def get_all_tickers(self):
        data_name_price, data_24hr = Crypto._get_all_stats_tickers()

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

    def get_one_ticket(self, symbol=""):
        """Выполняется это если была нажата кнопка поиска конкретной крипты"""

        data_name_price, data_24hr = Crypto._get_all_stats_tickers()
        for item_name_price in data_name_price:
            if item_name_price['symbol'] == symbol:
                for item_hr in data_24hr:
                    if item_hr['symbol'] == symbol:
                        item_name_price['change_24h'] = item_hr['priceChange']
                        return [item_name_price]
                return [{'symbol': 'Не найдено изменение цены за 24 часа'}]
        return [{'symbol': 'Криптовалюта не найдена в списке бинанса'}]


class Favorite_crypto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'crypto',)

    def __str__(self):
        return f'{self.user} ---- {self.crypto}'
