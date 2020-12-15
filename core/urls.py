from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('create-subscription', views.createSubscription, name='create-subscription'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('create-customer-stripe-session/', views.createcustomersession, name='session'),
    path('shipping/', views.ShippingView.as_view(), name='shipping'),
    path('webhooks/', views.webhook_view),

]
