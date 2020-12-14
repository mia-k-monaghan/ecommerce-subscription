from django.db import models
from django.conf import settings
from localflavor.us.models import USStateField,USZipCodeField
# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE, related_name='address')
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    state = USStateField()
    zip = USZipCodeField()

    def __str__(self):
        return self.street_address

        class Meta:
            verbose_name_plural = 'Shipping Addresses'

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    active = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, null=True, on_delete=models.SET_NULL)
    stripe_subscription = models.CharField(max_length=100,blank=True,
        help_text = "The user's Stripe Customer object, if it exists")
    last4 = models.CharField(max_length=4,blank=True,
        help_text = "The user's last 4 credit card digits, if they exist")

    def __str__(self):
        return str(self.user)
