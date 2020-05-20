from django.urls import path
from . import views

urlpatterns = [
    # path('', views.device_list),
    # path('<tankid>/', views.device_detail),
    path('<tankid>/data', views.get_tank_data)
]
