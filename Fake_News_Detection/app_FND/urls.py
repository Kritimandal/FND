from django.urls import path
from . import views

urlpatterns= [
    path('', views.FND, name="home")
    
]