from django.contrib import admin
from .models import Dokumen

@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ('nomor_surat', 'tanggal_surat', 'irban')  # Menampilkan kolom di daftar admin
    search_fields = ('nomor_surat', 'irban')  # Menambahkan pencarian
    list_filter = ('irban', 'tanggal_surat')  # Menambahkan filter di sidebar
    ordering = ('-tanggal_surat',)  # Mengurutkan berdasarkan tanggal terbaru
