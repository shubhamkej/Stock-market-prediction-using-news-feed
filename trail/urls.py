from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('trailapp.urls')),
    path('',include('accounts.urls')),
    path('',include('chartedData.urls')),
]
