from django.contrib import admin
from .models import Parcel, OriginalDocument


class TimestampsAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'created', 'modified')
    list_display_links = ('id', '__str__')

@admin.register(Parcel)
class ParcelAdmin(TimestampsAdmin):
    pass


@admin.register(OriginalDocument)
class OriginalDocumentAdmin(TimestampsAdmin):
    pass