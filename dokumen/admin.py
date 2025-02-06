from django.contrib import admin
from .models import Dokumen

@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ('nomor_surat', 'tanggal_surat', 'irban') 
    search_fields = ('nomor_surat', 'irban')  
    list_filter = ('irban', 'tanggal_surat') 
    ordering = ('-tanggal_surat',)
