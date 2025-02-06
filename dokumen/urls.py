from django.urls import path
from . import views
from .views import (
    unggah_dokumen, daftar_dokumen, unggah_laporan, 
    detail_dokumen, unduh_laporan, unduh_surat_tugas, ekspor_excel, create_user, update_user,  daftar_dokumen_admin, hapus_surat_tugas, hapus_laporan
)

urlpatterns = [

    path("ekspor/<str:rentang>/", ekspor_excel, name="ekspor_excel"),

    # ✅ Menampilkan daftar dokumen
    path("dokumen/daftar/", daftar_dokumen, name="daftar_dokumen"),

    # ✅ Menampilkan detail dokumen
    path("dokumen/<int:dokumen_id>/detail/", detail_dokumen, name="detail_dokumen"),

    # ✅ Mengunggah dokumen
    path("unggah/", unggah_dokumen, name="unggah_dokumen"),

    # ✅ Mengunggah laporan untuk dokumen tertentu
    path("unggah-laporan/<int:dokumen_id>/", unggah_laporan, name="unggah_laporan"),

    # ✅ Mengunduh surat tugas
    path("dokumen/<int:dokumen_id>/unduh/", unduh_surat_tugas, name="unduh_surat_tugas"),

    # ✅ Mengunduh laporan
    path("laporan/<int:laporan_id>/unduh/", unduh_laporan, name="unduh_laporan"),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('hapus_pengguna/<int:user_id>/', views.hapus_pengguna, name='hapus_pengguna'),
    path('hapus_dokumen/<int:dokumen_id>/', views.hapus_dokumen, name='hapus_dokumen'),

    path('admin/create-user/', create_user, name='create_user'),
    path('admin/update-user/<int:user_id>/', update_user, name='update_user'),

    path('admin/dokumen/', daftar_dokumen_admin, name='admin_daftar_dokumen'),
    path('admin/dokumen/hapus_surat/<int:dokumen_id>/', hapus_surat_tugas, name='hapus_surat_tugas'),

]
