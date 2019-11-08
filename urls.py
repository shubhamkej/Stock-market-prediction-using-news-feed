from django.urls import path, include
from . import views

urlpatterns = [
    path('graph/',views.graph,name='graph'),
]
