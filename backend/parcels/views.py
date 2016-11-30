from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import OriginalDocument


def original_document_list(request, template_name='parcels/original_document_list.html'):
    documents = OriginalDocument.objects.all()
    return render_to_response(template_name, locals())


def original_document_details(request, id, template_name='parcels/original_document_details.html'):
    document = OriginalDocument.objects.get(id=id)
    return render_to_response(template_name, locals())


def original_document_upload(request, template_name='parcels/original_document_upload.html'):
    return render_to_response(template_name, locals())