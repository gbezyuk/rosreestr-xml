from django.conf.urls import url
from .views import original_document_list, original_document_details, original_document_upload

urlpatterns = [
    url(r'^$', original_document_list, name='original_document_list'),
    url(r'^upload/$', original_document_upload, name='original_document_upload'),
    url(r'^(?P<id>[0-9]+)/$', original_document_details, name='original_document_details'),
]
