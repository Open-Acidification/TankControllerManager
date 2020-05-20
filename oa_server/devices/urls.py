from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list),
    path('<mac>/', views.device_detail),
    path('<mac>/data', views.get_device_data)
]
