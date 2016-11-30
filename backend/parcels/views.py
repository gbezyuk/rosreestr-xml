from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CadastralBlock, Parcel
from .forms import CadastralBlockFileUploadForm


def cadastral_block_list(request, template_name='parcels/cadastral_block_list.html'):
    cadastral_blocks = CadastralBlock.objects.all()
    return render_to_response(template_name, locals())


def cadastral_block_details(request, id, template_name='parcels/cadastral_block_details.html'):
    cadastral_block = CadastralBlock.objects.get(id=id)
    return render_to_response(template_name, locals())


@csrf_exempt
def cadastral_block_upload(request, template_name='parcels/cadastral_block_upload.html'):
    if request.method == 'POST':
        form = CadastralBlockFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_block = CadastralBlock.handle_uploaded_file(request.FILES['file'])
            return redirect(new_block.get_absolute_url(), permanent=False)
    else:
        form = CadastralBlockFileUploadForm()
    return render_to_response(template_name, locals())


def parcel_details(request, id, template_name='parcels/parcel_details.html'):
    parcel = Parcel.objects.get(id=id)
    return render_to_response(template_name, locals())