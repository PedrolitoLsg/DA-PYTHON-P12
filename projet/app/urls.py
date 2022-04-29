from django.contrib import admin
from django.urls import include, re_path
from django.conf import settings


urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('', include('db.urls')),
]
