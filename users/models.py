from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
# class UserManager(BaseUserManager):
#     """Define a model manager for User model with no username field."""
#
#     use_in_migrations = True
#
#     def _create_user(self, email, password, **extra_fields):
#         """Create and save a User with the given email and password."""
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password=None, **extra_fields):
#         """Create and save a regular User with the given email and password."""
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         """Create and save a SuperUser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    pass
    # username = None
    # email = models.EmailField(_('email address'), unique=True)
    # stripe_customer = models.CharField(max_length=100,blank=True,
    #     help_text = "The user's Stripe Customer object, if it exists")
    #
    #
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS
    #
    # objects = UserManager()
    #
    # def __str__(self):
    #     return (self.email)
