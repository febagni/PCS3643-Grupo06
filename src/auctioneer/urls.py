from django.urls import path

from . import views

app_name = 'auctioneer'

urlpatterns = [
  path('', views.auction_list, name='auction_list'),
  path('new/', views.auction_create, name='auction_new'),
  path('list_lot/', views.auction_list_lot, name='auction_list_lot'),
  path('add_lot/<int:id>/<int:pk>/', views.auction_add_lot, name='auction_add_lot'),
  path('publish/<int:pk>/', views.auction_publish, name='auction_publish'),
  path('cancel/<int:pk>/', views.auction_cancel, name='auction_cancel'),
  path('edit/<int:pk>/', views.auction_update, name='auction_edit'),
  path('delete/<int:pk>/', views.auction_delete, name='auction_delete'),
  path('performance_rep/<int:pk>/', views.auction_performance_report, name='auction_performance_report'),
  path('financial_rep/<int:pk>/', views.auction_financial_report, name='auction_financial_report'),
  path('full_performance_rep/', views.full_performance_report, name='full_performance_report'),
  path('full_financial_rep/', views.full_financial_report, name='full_financial_report')

]
