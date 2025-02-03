from django import forms
from .models import Dokumen

class DokumenForm(forms.ModelForm):
    class Meta:
        model = Dokumen
        fields = ['nomor_surat', 'judul', 'jenis', 'file']  # Menambahkan nomor_surat, judul, dan jenis dokumen
