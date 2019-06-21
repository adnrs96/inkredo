from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models

# Create your models here.

class Company(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(blank=False, unique=True)
    name = models.CharField(max_length=50)
    registered_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)

    PUBLIC = 1
    PRIVATE = 2

    COMPANY_TYPES = (
        (PUBLIC, 'A company whose shares may not be offered to the public for sale.'),
        (PRIVATE, 'A company whose shares are traded freely on a stock exchange.'),
    )

    type = models.PositiveSmallIntegerField(
        choices=COMPANY_TYPES,
        default=PRIVATE
    )
    objects = UserManager()

class User(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=50)
    company = models.ForeignKey(
        Company,
        related_name='company_users',
        on_delete=models.SET_NULL,
        null=True,
    )
    objects = UserManager()
