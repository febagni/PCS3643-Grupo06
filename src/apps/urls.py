from django.urls import include, path
from django.contrib import admin

import theme.views

urlpatterns = [
    path('', theme.views.home),
    path('lot/', include('lot.urls')),
    path('lot_user/', include('lot_user.urls')),
    #path('auction/', include('auction.urls')),
    #path('auctioneer/', include('auctioneer.urls')),

    # Enable built-in authentication views
    path('accounts/', include('django.contrib.auth.urls')),    
    # Enable built-in admin interface
    path('admin/', admin.site.urls),
]
