from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import CadastralBlock, Parcel
from .forms import CadastralBlockFileUploadForm
from django.http import HttpResponse


def cadastral_block_list(request, template_name='parcels/cadastral_block_list.html'):
    cadastral_blocks = CadastralBlock.objects.all()
    return render_to_response(template_name, locals())


def cadastral_block_details(request, id, template_name='parcels/cadastral_block_details.html'):
    cadastral_block = get_object_or_404(CadastralBlock, id=id)
    return render_to_response(template_name, locals())


def cadastral_block_csv(request, id):
    cadastral_block = get_object_or_404(CadastralBlock, id=id)    
    response = HttpResponse(content_type='text/csv',
                            content=open(cadastral_block.get_csv_representation_file_path(), 'rt'))
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' %\
                                      cadastral_block.cadastral_number.replace(':', '_')
    return response


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
    parcel = get_object_or_404(Parcel, id=id)
    return render_to_response(template_name, locals())


def parcel_csv(request, id):
    parcel = get_object_or_404(Parcel, id=id)
    response = HttpResponse(content_type='text/csv',
                            content=open(parcel.get_csv_representation_file_path(), 'rt'))
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' %\
                                      parcel.cadastral_number.replace(':', '_')
    return response
    