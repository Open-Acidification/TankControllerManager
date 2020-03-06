from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue, name='vue'),
]