from django.urls import path

from lot import views

app_name = 'lot'

urlpatterns = [
  path('', views.lot_list, name='lot_list'),
  path('new/', views.lot_create, name='lot_new'),
  path('edit/<int:pk>/', views.lot_update, name='lot_edit'),
  path('delete/<int:pk>/', views.lot_delete, name='lot_delete'),
]