from django.urls import path
from .views import unggah_dokumen, daftar_dokumen, unduh_dokumen

urlpatterns = [
    path('unduh/<int:dokumen_id>/', unduh_dokumen, name='unduh_dokumen'),
    path('unggah/', unggah_dokumen, name='unggah_dokumen'),
    path('daftar/', daftar_dokumen, name='daftar_dokumen'),  # Tambahkan URL ini
]
