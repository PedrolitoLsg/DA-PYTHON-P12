from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from .managers import CustomUsersManager
from django.contrib.auth.models import PermissionsMixin

support_choices = [
    ('UNDEFINED', "0"),
    ('PAUL', "1"),
    ('TOM', "2")
]

event_status = [
    ('open', '0'),
    ('closed', '1')
]

contract_status = [
    ('unsigned', '0'),
    ('signed', '1')
]

roles_list = [
    ('Sales', 'sales'),
    ('Support', 'support')
]


class CustomUsers(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = None
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    password = models.TextField(max_length=40)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    role = models.CharField(max_length=25, choices=roles_list, null=False)

    objects = CustomUsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    list_filter = ('staff', 'admin')
    list_display = ('user_id', 'first-name', 'last_name')
    ordering = 'user_id'

    @property
    def is_staff(self):
        return self.staff



class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250,
                                    default='To Be Defined'
                                    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    sales = models.ForeignKey(to=CustomUsers, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Contract(models.Model):
    value = models.IntegerField()
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    sales = models.ForeignKey(to=CustomUsers, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=124,
                              choices=contract_status,
                              default='unsigned')



class Event(models.Model):
    title = models.CharField(max_length=50, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    contract = models.OneToOneField(Contract,
                                 on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    support = models.ForeignKey(to=CustomUsers, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50,
                              choices=event_status,
                              default='open')
