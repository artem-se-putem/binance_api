from django.contrib import admin
from .models import Crypto, Favorite_crypto


admin.site.register(Crypto)
admin.site.register(Favorite_crypto)
