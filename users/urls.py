from django.urls import path
from .views import SignupView, LoginView,ProfileView, ProfileUpdate, ShippingUpdateView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/<pk>',ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<pk>/profile-update/',ProfileUpdate.as_view(), name='profile-update'),
    path('profile/<pk>/shipping-update/',ShippingUpdateView.as_view(), name='shipping-update'),

]
