from django.contrib import admin
from .models import CustomUsers, Contract, Event, Customer


admin.site.register(CustomUsers)
admin.site.register(Contract)
admin.site.register(Event)
admin.site.register(Customer)
