from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.views.generic import View
from django.views.generic.base import TemplateView
from .models import Subscription
from .forms import AddressForm

import json
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Create your views here.
class IndexView(TemplateView):
    template_name = 'core/index.html'

class ShippingView(LoginRequiredMixin, View):

    def get(self, *args,**kwargs):
        form = AddressForm()

        context= {
            'form':form,
        }
        return render(self.request, 'core/shipping.html', context)

    def post(self, *args, **kwargs):
        form = AddressForm(self.request.POST)


        if form.is_valid():
            # save address in address model
            new_address = form.save(commit=False)
            new_address.user = self.request.user
            new_address.save()

            # update subscription model with address
            dj_subscription = Subscription.objects.get(user=self.request.user)
            dj_subscription.shipping_address=new_address
            dj_subscription.save()

        return HttpResponseRedirect(reverse('core:checkout'))

class CheckoutView(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        return render(self.request, 'core/subscribe.html')

class SuccessView(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        return render(self.request, 'core/success.html')


@csrf_exempt
@login_required
def createSubscription(request):
    if request.method=="POST":
        data = json.loads(request.body)
        try:
            # Attach the payment method to the customer
            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=request.user.stripe_customer,
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                request.user.stripe_customer,
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            # Create the subscription
            subscription = stripe.Subscription.create(
                customer=request.user.stripe_customer,
                items=[
                    {
                        'price': data['priceId']
                    }
                ],
                expand=['latest_invoice.payment_intent'],
            )

            # Update the local subscription models
            dj_subscription = Subscription.objects.get(user=request.user)
            try:
                dj_subscription.stripe_subscription = subscription.id
                dj_subscription.active = True
                dj_subscription.last4 = data['last4']
                dj_subscription.save()

            except ObjectDoesNotExist:
                print("could not find user object")

            return JsonResponse(subscription)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e)}, status=200)

@login_required
def createcustomersession(request):
    user = stripe.Customer.retrieve(request.user.stripe_customer)
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

    session = stripe.billing_portal.Session.create(
      customer=user.id,
      return_url= 'http://127.0.0.1:8000/',

    )
    return HttpResponseRedirect(session.url)

@require_POST
@csrf_exempt
def webhook_view(request):
    payload=request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload,sig_header, settings.STRIPE_SIGNING_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    if event['type']=='customer.subscription.deleted':
        stripe_sub = event['data']['object']
        sub = Subscription.objects.get(stripe_subscription=stripe_sub['id'])
        sub.active = False
        sub.save()
        print('Subscription Inactive')

    else:
        pass
    return HttpResponse(status=200)
