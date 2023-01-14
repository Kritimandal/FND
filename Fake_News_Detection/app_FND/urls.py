from django.urls import path
from . import views

urlpatterns= [
    path('fakenewsdetection', views.FND, name='fnd'),
]