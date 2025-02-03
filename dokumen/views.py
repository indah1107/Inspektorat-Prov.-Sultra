from django.shortcuts import render, redirect
from .forms import DokumenForm
from django.contrib import messages
from .models import Dokumen


from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
import os
from .models import Dokumen

def daftar_dokumen(request):
    # Ambil parameter pencarian dari GET request
    nomor_surat = request.GET.get('nomor_surat', '')
    judul = request.GET.get('judul', '')
    jenis = request.GET.get('jenis', '')

    # Filter dokumen berdasarkan pencarian
    dokumen_list = Dokumen.objects.all()

    if nomor_surat:
        dokumen_list = dokumen_list.filter(nomor_surat__icontains=nomor_surat)
    if judul:
        dokumen_list = dokumen_list.filter(judul__icontains=judul)
    if jenis:
        dokumen_list = dokumen_list.filter(jenis__icontains=jenis)

    # Render halaman dengan daftar dokumen yang difilter
    return render(request, 'dokumen/daftar_dokumen.html', {'dokumen_list': dokumen_list})

def unduh_dokumen(request, dokumen_id):
    dokumen = get_object_or_404(Dokumen, id=dokumen_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(dokumen.file))
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse("File tidak ditemukan", status=404)

def unggah_dokumen(request):
    if request.method == 'POST':
        form = DokumenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Simpan dokumen
            messages.success(request, 'Dokumen berhasil diunggah!')
            return redirect('dashboard')  # Redirect setelah sukses
        else:
            messages.error(request, 'Terjadi kesalahan saat mengunggah dokumen.')
    else:
        form = DokumenForm()

    return render(request, 'dokumen/unggah_dokumen.html', {'form': form})

