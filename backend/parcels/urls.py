from django.conf.urls import url
from .views import cadastral_block_list, cadastral_block_details,\
                   cadastral_block_upload, cadastral_block_csv,\
                   parcel_details, parcel_csv

urlpatterns = [
    url(r'^$', cadastral_block_list, name='cadastral_block_list'),
    url(r'^upload/$', cadastral_block_upload, name='cadastral_block_upload'),
    url(r'^(?P<id>[0-9]+)/$', cadastral_block_details, name='cadastral_block_details'),
    url(r'^(?P<id>[0-9]+)/csv/$', cadastral_block_csv, name='cadastral_block_csv'),
    url(r'^parcels/(?P<id>[0-9]+)/$', parcel_details, name='parcel_details'),
    url(r'^parcels/(?P<id>[0-9]+)/csv/$', parcel_csv, name='parcel_csv'),
]
