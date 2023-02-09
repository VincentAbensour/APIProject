from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self,firstname,lastname,email,password=None):
        """Create new basic user"""
        if not email:
            raise ValueError("Email adress is missing")

        user = self.model(
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,firstname,lastname,email,password):
        """Create new superuser"""
        user=self.create_user(
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            password = password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True


        user.save()
        return user

class Account(AbstractBaseUser,PermissionsMixin):
    """Custom Account Class"""
    email = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["firstname", "lastname"]

    objects = AccountManager()

    def __str__(self):
        return self.email
