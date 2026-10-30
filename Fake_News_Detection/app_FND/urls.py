from django.urls import path
from . import views

urlpatterns = [
    path('', views.FND, name='home'),
    path('api/predict/', views.predict_api, name='predict-api'),
]
