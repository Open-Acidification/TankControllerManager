from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_tanks),
    path('<tankid>/', views.manage_tank),
    path('<tankid>/data', views.get_tank_data),
    path('<tankid>/history', views.get_tank_history)
]
