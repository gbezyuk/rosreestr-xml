from django.conf.urls import url
from .views import cadastral_block_list, cadastral_block_details, cadastral_block_upload, parcel_details

urlpatterns = [
    url(r'^$', cadastral_block_list, name='cadastral_block_list'),
    url(r'^upload/$', cadastral_block_upload, name='cadastral_block_upload'),
    url(r'^(?P<id>[0-9]+)/$', cadastral_block_details, name='cadastral_block_details'),
    url(r'^parcels/(?P<id>[0-9]+)/$', parcel_details, name='parcel_details'),
]
