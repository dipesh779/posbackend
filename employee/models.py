import datetime
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import Group


from libs.validators import PHONE_REGEX
from libs.constants import EMPLOYEE_TYPE_CHOICES


class EUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Mobile Number must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    company = models.ForeignKey('database.CompanyDetail', on_delete=models.CASCADE, related_name='employee', null=True)
    branchh = models.ForeignKey('database.Branch', on_delete=models.CASCADE, related_name='employee', null=True)
    employee_id = models.CharField(max_length=50)
    employee_type = models.CharField(max_length=50, choices=EMPLOYEE_TYPE_CHOICES, default='staff')
    employee_name = models.CharField(max_length=50)
    employee_position = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    dob = models.DateField(default=datetime.date(1996, 1, 1))
    phone = models.CharField(max_length=15, validators=[PHONE_REGEX])
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField('staff status', default=False, null=True,
                                   help_text='Designates whether the user can log into this site.')
    is_active = models.BooleanField('active', default=True, null=True,
                                    help_text='Designates whether this user should be treated as active. '
                                              'Unselect this instead of deleting accounts.')
    objects = EUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.employee_name


    



