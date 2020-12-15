from django.urls import path
from .views import SignupView, LoginView,ProfileView, ProfileUpdate, ShippingUpdateView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('', SignupView.as_view(), name='index'),
    path('profile/<pk>',ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile-update/<pk>',ProfileUpdate.as_view(), name='profile-update'),
    path('shipping-update/<pk>',ShippingUpdateView.as_view(), name='shipping-update'),

]
