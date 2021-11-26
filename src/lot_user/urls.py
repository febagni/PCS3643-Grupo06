from django.urls import path

from . import views

app_name = 'lot_user'

urlpatterns = [
  path('', views.lot_list, name='lot_list'),
  path('new/', views.lot_create, name='lot_new'),
  path('detail/<int:pk>/', views.lot_detail, name='lot_detail'),
  path('edit/<int:pk>/', views.lot_update, name='lot_edit'),
  path('delete/<int:pk>/', views.lot_delete, name='lot_delete'),
  path('remove/<int:pk>/', views.lot_remove, name='lot_remove'),
]
