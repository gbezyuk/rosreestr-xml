from django.conf.urls import url
from .views import cadastral_block_list, cadastral_block_details, cadastral_block_upload

urlpatterns = [
    url(r'^$', cadastral_block_list, name='original_document_list'),
    url(r'^upload/$', cadastral_block_upload, name='original_document_upload'),
    url(r'^(?P<id>[0-9]+)/$', cadastral_block_details, name='original_document_details'),
]
