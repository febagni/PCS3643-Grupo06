from django.urls import path

from . import views

app_name = 'buyer'

urlpatterns = [
  path('bid/<int:pk>/', views.bid_request, name='bid_request'),
]
