from django.urls import path

from auction import views

app_name = 'auction'

urlpatterns = [
  path('', views.auction_list, name='auction_list'),
  path('new/', views.auction_create, name='auction_new'),
  path('edit/<int:pk>/', views.auction_update, name='auction_edit'),
  path('delete/<int:pk>/', views.auction_delete, name='auction_delete'),
]