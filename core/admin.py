from django.contrib import admin
from .models import Subscription, ShippingAddress
# Register your models here.

admin.site.register(Subscription)
admin.site.register(ShippingAddress)
