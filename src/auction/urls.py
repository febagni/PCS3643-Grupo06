from django.urls import path

from auction import views

app_name = 'auction'

urlpatterns = [
  path('', views.auction_list, name='auction_list'),
  path('bid/<int:id>/<int:pk>/', views.make_bid, name='make_bid'),
]