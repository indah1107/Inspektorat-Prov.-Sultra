from django import forms
from .models import Dokumen, Laporan
import json  # Untuk memproses data JSON

class DokumenForm(forms.ModelForm):
    IRBAN_CHOICES = [
        ("IRBAN 1", "IRBAN 1"),
        ("IRBAN 2", "IRBAN 2"),
        ("IRBAN 3", "IRBAN 3"),
        ("IRBAN 4", "IRBAN 4"),
        ("IRBAN INVESTIGASI", "IRBAN INVESTIGASI"),
    ]

    irban = forms.ChoiceField(choices=IRBAN_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    tim_audit = forms.CharField(widget=forms.HiddenInput(), required=False)  # Data JSON dari JavaScript

    class Meta:
        model = Dokumen
        fields = ["nomor_surat", "tanggal_surat", "irban", "tim_audit", "uraian", "file"]
        widgets = {
            "nomor_surat": forms.TextInput(attrs={"class": "form-control", "placeholder": "Masukkan nomor surat"}),
            "tanggal_surat": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_tim_audit(self):
        """Pastikan tim audit berbentuk JSON valid."""
        tim_audit_data = self.cleaned_data.get("tim_audit")
        try:
            if tim_audit_data:
                return json.loads(tim_audit_data)  # Konversi dari string ke JSON
            return []
        except json.JSONDecodeError:
            raise forms.ValidationError("Format data tim audit tidak valid.")


class LaporanForm(forms.ModelForm):
    class Meta:
        model = Laporan
        fields = ['judul_laporan', 'tanggal_laporan', 'nomor_laporan', 'keterangan', 'file']

    def __init__(self, *args, **kwargs):
        """Pastikan dokumen terhubung dengan laporan"""
        self.dokumen_instance = kwargs.pop('dokumen', None)  # Ambil dokumen yang dikirim dari view
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Gabungkan data laporan dengan dokumen sebelum menyimpan."""
        laporan = super().save(commit=False)
        if self.dokumen_instance:
            laporan.dokumen = self.dokumen_instance  # Hubungkan laporan dengan dokumen yang sedang diunggah
        if commit:
            laporan.save()
        return laporan
