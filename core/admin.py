from django.contrib import admin
from .models import Subscription, ShippingAddress
# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):

    list_filter = ['active']
    search_fields = ['user__email', 'shipping_address__state','user__stripe_customer','stripe_subscription']
    list_display = ['user','shipping_address', 'active']
    list_display_links = ['user','shipping_address']

class ShippingAddressAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'city','state','user__stripe_customer','zip','street_address']
    list_display = ['user','street_address','city','state','zip']
    list_display_links = ['user']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
