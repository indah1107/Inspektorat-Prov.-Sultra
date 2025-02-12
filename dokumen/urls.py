from django.urls import path
from . import views
from .views import (
    unggah_dokumen, daftar_dokumen, unggah_laporan, 
    detail_dokumen, unduh_laporan, unduh_surat_tugas, ekspor_excel, create_user, update_user,  daftar_dokumen_admin,
)

urlpatterns = [
    path('daftar_dokumen/', views.daftar_dokumen, name='daftar_dokumen'),
    path('ekspor_excel/', views.ekspor_excel, name='ekspor_excel'),
    path("dokumen/daftar/", daftar_dokumen, name="daftar_dokumen"),
    path("dokumen/<int:dokumen_id>/detail/", detail_dokumen, name="detail_dokumen"),
    path("unggah/", unggah_dokumen, name="unggah_dokumen"),
    path("unggah-laporan/<int:dokumen_id>/", unggah_laporan, name="unggah_laporan"),
    path("dokumen/<int:dokumen_id>/unduh/", unduh_surat_tugas, name="unduh_surat_tugas"),
    path("laporan/<int:laporan_id>/unduh/", unduh_laporan, name="unduh_laporan"),
    path('hapus_pengguna/<int:user_id>/', views.hapus_pengguna, name='hapus_pengguna'),
    path('hapus_dokumen/<int:dokumen_id>/', views.hapus_dokumen, name='hapus_dokumen'),
    path('admin/create-user/', create_user, name='create_user'),
    path('admin/update-user/<int:user_id>/', update_user, name='update_user'),
    path('admin/dokumen/', daftar_dokumen_admin, name='admin_daftar_dokumen'),

]
