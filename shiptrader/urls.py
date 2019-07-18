from django.conf.urls import url, include
from django.contrib import admin

from shiptrader import views

urlpatterns = [
    url(r'^starships/$', views.StarShipsAPI.as_view(), name='starships'),
    url(r'^starships/(?P<ship_id>[0-9]+)/$', views.StarShipAPI.as_view(), name='starship'),

    url(r'^listings/$', views.ListingsAPI.as_view(), name='listings'),
    url(r'^listings/(?P<listing_id>[0-9]+)/$', views.ListingAPI.as_view(), name='listing'),
    url(
        r'^listings/(?P<listing_id>[0-9]+)/action/(?P<action>activate|deactivate)/$',
        views.ListingAPIActions.as_view(),
        name='listing-actions'
    ),
]