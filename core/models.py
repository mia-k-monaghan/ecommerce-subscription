from django.db import models
from localflavor.us.models import USStateField,USZipCodeField
from django.conf import settings
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
