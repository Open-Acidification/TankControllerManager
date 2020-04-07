from django.urls import path
from . import views

urlpatterns = [
    path('', views.time_series_list),
    path('generate/hold/', views.time_series_generate_hold),
    path('generate/ramp/', views.time_series_generate_ramp),
    path('generate/sine/', views.time_series_generate_sine),
    path('<int:id>/', views.time_series_detail),
]
