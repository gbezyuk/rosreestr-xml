from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from .models import Parcel, CadastralBlock


# class TimestampsAdmin(admin.ModelAdmin):
#     list_display = ('id', '__str__', 'created', 'modified')
#     list_display_links = ('id', '__str__')


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ('id', 'cadastral_number', 'utilization', 'block', 'created', 'modified')
    list_display_links = ('id', 'cadastral_number')
    readonly_fields = ('cadastral_number', 'utilization', 'path_json', 'block')
    list_filter  = ('block', 'utilization')
    search_fields = ('cadastral_number', 'utilization')
    date_hierarchy = 'created'


class ParcelInline(admin.TabularInline):
    model = Parcel
    readonly_fields = ('cadastral_number', 'utilization', 'path_json', 'block')


@admin.register(CadastralBlock)
class CadastralBlockAdmin(admin.ModelAdmin):
    inlines = [ParcelInline]
    list_display = ('id', 'cadastral_number', 'root_node_name', 'status', 'original_file_size_humanized', 'created', 'modified')
    list_display_links = ('id', 'cadastral_number')
    readonly_fields = ('cadastral_number', 'root_node_name', 'status', 'file', 'original_file_size', 'original_file_name')
    list_filter = ('root_node_name', 'status')
    search_fields = ('cadastral_number', 'utilization')
    date_hierarchy = 'created'

    def original_file_size_humanized(self, block):
        return filesizeformat(block.original_file_size)
    original_file_size_humanized.short_descriptoin = _('original file size')