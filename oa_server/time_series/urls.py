from django.urls import path
from . import views

urlpatterns = [
    path('', views.time_series_save),
    path('<str:ts_type>/', views.time_series_list),
    path('<str:ts_type>/generate/hold/', views.time_series_generate_hold),
    path('<str:ts_type>/generate/ramp/', views.time_series_generate_ramp),
    path('<str:ts_type>/generate/sine/', views.time_series_generate_sine),
    path('<int:id>/', views.time_series_detail),
]
