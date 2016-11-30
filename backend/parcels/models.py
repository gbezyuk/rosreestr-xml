from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.conf import settings
from django.urls import reverse
import os


class TimestampsModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('-modified',)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class CadastralBlock(TimestampsModel):
    class Meta(TimestampsModel.Meta):
        verbose_name = _('Cadastral Block')
        verbose_name_plural = _('Cadastral Blocks')

    # TODO: store file size in a separate field
    file = models.FileField(verbose_name=_('file'), max_length=500, upload_to=settings.CADASTRAL_BLOCK_UPLOAD_TO)
    original_file_name = models.CharField(verbose_name=_('original file name'), max_length=100)
    cadastral_number = models.CharField(verbose_name=_('cadastral number'), max_length=40, null=True, blank=True)

    def __str__(self):
        return __("Cadastral block %s (%d)" % (self.cadastral_number or '', self.id))

    @staticmethod
    def handle_uploaded_file(file_object):
        if file_object.content_type != 'text/xml':
            raise ValueError('only xml files are accepted')
        with open(os.path.join(settings.CADASTRAL_BLOCK_FILE_UPLOAD_DIR, file_object.name), 'wb+') as destination:
            for chunk in file_object.chunks():
                destination.write(chunk)
        new_block = CadastralBlock(
            file=os.path.join(settings.CADASTRAL_BLOCK_UPLOAD_TO, file_object.name),
            original_file_name=file_object.name)
        new_block.save()
        return new_block

    def get_absolute_url(self):
        return reverse('cadastral_block_details', args=[str(self.id)])



class Parcel(TimestampsModel):
    class Meta(TimestampsModel.Meta):
        verbose_name = _('Parcel')
        verbose_name_plural = _('Parcels')

    document = models.ForeignKey(to=CadastralBlock, verbose_name=_('document'))
    cadastral_number = models.CharField(verbose_name=_('cadastral number'), max_length=40)
    utilization = models.CharField(verbose_name=_('utilization'), max_length=200)
    json_representation = models.TextField(verbose_name=_('JSON representation'))

    def __str__(self):
        return __("Parcel %s (%d)" % (self.cadastral_number or '', self.id))

    def get_absolute_url(self):
        return reverse('parcel_details', args=[str(self.id)])