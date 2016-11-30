from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.conf import settings
from django.urls import reverse
import json
import os
from .parser import get_parcels_and_metadata, store_as_csv


class TimestampsModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('-modified',)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)


class CadastralBlock(TimestampsModel):
    class Meta(TimestampsModel.Meta):
        verbose_name = _('Cadastral Block')
        verbose_name_plural = _('Cadastral Blocks')

    file = models.FileField(verbose_name=_('file'), max_length=500,
                            upload_to=settings.CADASTRAL_BLOCK_UPLOAD_TO)
    original_file_name = models.CharField(verbose_name=_('original file name'), max_length=100)
    original_file_size = models.PositiveIntegerField(verbose_name=_('original file size'))
    cadastral_number = models.CharField(verbose_name=_('cadastral number'),
                                        max_length=40, null=True, blank=True)

    def __str__(self):
        return __("Cadastral block %s (%d)" % (self.cadastral_number or '', self.id))

    def get_absolute_url(self):
        return reverse('cadastral_block_details', args=[str(self.id)])

    @staticmethod
    def handle_uploaded_file(file_object):
        if file_object.content_type != 'text/xml':
            raise ValueError('only xml files are accepted')
        with open(os.path.join(settings.CADASTRAL_BLOCK_FILE_UPLOAD_DIR,
                               file_object.name), 'wb+') as destination:
            for chunk in file_object.chunks():
                destination.write(chunk)
        new_block = CadastralBlock()
        new_block.file = os.path.join(settings.CADASTRAL_BLOCK_UPLOAD_TO, file_object.name)
        new_block.original_file_name = file_object.name
        new_block.original_file_size = file_object.size
        new_block.save()
        new_block.parse_file()
        return new_block

    @property
    def full_file_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.file.name) if self.file else None

    def parse_file(self):
        parcels, metadata = get_parcels_and_metadata(self.full_file_path)
        self.cadastral_number = metadata['cadastral_number']
        self.save()
        for parcel_data in parcels:
            new_parcel = Parcel()
            new_parcel.block = self
            new_parcel.cadastral_number = parcel_data['cadastral_number']
            new_parcel.utilization = parcel_data['utilization']
            new_parcel.path_json = json.dumps(parcel_data['path'], sort_keys=True, indent=4)
            new_parcel.save()


class Parcel(TimestampsModel):
    class Meta(TimestampsModel.Meta):
        verbose_name = _('Parcel')
        verbose_name_plural = _('Parcels')

    block = models.ForeignKey(to=CadastralBlock, verbose_name=_('block'), related_name='parcels')
    cadastral_number = models.CharField(verbose_name=_('cadastral number'), max_length=40)
    utilization = models.CharField(verbose_name=_('utilization'), max_length=200)
    path_json = models.TextField(verbose_name=_('path JSON'))

    def __str__(self):
        return __("Parcel %s (%d)" % (self.cadastral_number or '', self.id))

    def get_absolute_url(self):
        return reverse('parcel_details', args=[str(self.id)])
