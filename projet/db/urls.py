from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, include
from .views import Customers, SoloCustomer, Events, SoloEvent, Contracts, SoloContract, Main, UserRegistrationView
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout, login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import TokenObtainPairView


app_name = 'db'

urlpatterns = [
    re_path('main', Main, name='main'),
    re_path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('new_user/', UserRegistrationView.as_view({'post': 'create'})),
    re_path('login/', TokenObtainPairView.as_view(), name='login'),
    re_path('customers/$', Customers.as_view({'get': 'list', 'post': 'create', 'put':'update'})),
    re_path('customers/(?P<customer_id>[0-9])/$', SoloCustomer.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    re_path('contracts/$', Contracts.as_view({'get': 'list', 'post': 'create'})),
    re_path('contracts/(?P<contract_id>[0-9])/$', SoloContract.as_view({'get': 'retrieve', 'put':'update', 'delete': 'destroy'})),
    re_path('events/$', Events.as_view({'get': 'list', 'post':'create'}), name='events_list'),
    re_path('events/(?P<event_id>[0-9])/$', SoloEvent.as_view({'get': 'retrieve', 'put': 'update', 'delete':'destroy'}))
]