from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimestampsModel(models.Model):
    class Meta:
        abstract = True
        ordering = ('-modified',)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class OriginalDocument(TimestampsModel):
    file = models.FileField(verbose_name=_('file'), max_length=500)
    original_file_name = models.CharField(verbose_name=_('original file name'), max_length=100)
    cadastral_number = models.CharField(verbose_name=_('cadastral number'), max_length=40)


class Parcel(TimestampsModel):
    class Meta(TimestampsModel.Meta):
        verbose_name = _('Parcel')
        verbose_name_plural = _('Parcels')

    document = models.ForeignKey(to=OriginalDocument, verbose_name=_('document'))
    cadastral_number = models.CharField(verbose_name=_('cadastral number'), max_length=40)
    json_representation = models.TextField(verbose_name=_('CSV representation'))