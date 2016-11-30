from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import CadastralBlock


def cadastral_block_list(request, template_name='parcels/cadastral_block_list.html'):
    documents = CadastralBlock.objects.all()
    return render_to_response(template_name, locals())


def cadastral_block_details(request, id, template_name='parcels/cadastral_block_details.html'):
    document = CadastralBlock.objects.get(id=id)
    return render_to_response(template_name, locals())


def cadastral_block_upload(request, template_name='parcels/cadastral_block_upload.html'):
    return render_to_response(template_name, locals())