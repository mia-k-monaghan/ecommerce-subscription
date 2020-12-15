from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from core.models import Subscription, ShippingAddress
from core.forms import AddressForm
from .forms import SignUpForm, LoginForm

import stripe
# Create your views here.

class SignupView(CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        return reverse_lazy('core:shipping')

    def form_valid(self, form):
        stripe.api_key=settings.STRIPE_TEST_SECRET_KEY
        valid = super(SignupView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        user = authenticate(email=email,
                            password=password)
        login(self.request, user)

        new_stripe_cust = stripe.Customer.create(
            email=email,
            name=form.cleaned_data.get('first_name') + " " + form.cleaned_data.get('last_name')
        )
        Subscription.objects.create(
            user=self.request.user,
            )
        self.request.user.stripe_customer = new_stripe_cust.id
        self.request.user.save()


        return valid

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})

class ProfileView(View, LoginRequiredMixin):

    def get(self, *args, **kwargs):
        user = self.request.user

        try:
            address = Subscription.objects.get(user=self.request.user).address

            context = {
                'user':user,
                'last4': user.last4,
                'address_pk': address.pk,
                'street_address':address.street_address,
                'apt_address':address.apartment_address,
                'city':address.city,
                'state':address.state,
                'zip':address.zip,
            }
        except ObjectDoesNotExist:
            context = {}

        return render(self.request, 'users/profile.html', context)

class ProfileUpdate(UpdateView):
    model = CustomUser
    template_name = 'users/user_update.html'
    fields = ['first_name', 'last_name', 'email',]

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('users:profile',args=[pk])

class ShippingUpdateView(LoginRequiredMixin, UpdateView):
    model=ShippingAddress
    form_class = AddressForm
    template_name = 'core/shipping_update.html'


    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('users:profile',args=[pk])
