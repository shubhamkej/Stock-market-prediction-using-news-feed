from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('tweets/',views.tweets,name='tweets'),
    path('stocks/',views.stocks,name='stocks'),
    path('historical/',views.historical,name='historical'),

]
