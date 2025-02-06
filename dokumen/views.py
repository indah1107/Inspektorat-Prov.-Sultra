from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Dokumen, Laporan
from .forms import DokumenForm, LaporanForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json

# ✅ UNGGAH SURAT TUGAS
def unggah_dokumen(request):
    if request.method == "POST":
        form = DokumenForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Dokumen berhasil diunggah.")
                return redirect("unggah_dokumen")
            except IntegrityError:
                messages.error(request, "Nomor surat sudah digunakan. Gunakan nomor yang berbeda.")

            dokumen = form.save(commit=False)

            # 🔹 Konversi data tim_audit ke JSON jika dikirim sebagai string JSON
            tim_audit_data = request.POST.get("tim_audit")
            if tim_audit_data:
                try:
                    dokumen.tim_audit = json.loads(tim_audit_data)
                except json.JSONDecodeError:
                    dokumen.tim_audit = []  # Jika gagal, set default kosong

            dokumen.save()
            messages.success(request, "Surat Tugas berhasil diunggah.")
            return redirect("dashboard")
        else:
            print("Form Errors:", form.errors)  # Debug error
            messages.error(request, "Terjadi kesalahan, pastikan semua data telah diisi dengan benar.")
    else:
        form = DokumenForm()

    return render(request, "dokumen/unggah_dokumen.html", {"form": form})

# ✅ UNGGAH & UPDATE LAPORAN
def unggah_laporan(request, dokumen_id):
    dokumen = get_object_or_404(Dokumen, id=dokumen_id)

    # Cek apakah laporan sudah ada untuk dokumen ini, jika tidak, buat baru
    laporan, created = Laporan.objects.get_or_create(dokumen=dokumen)

    if request.method == "POST":
        form = LaporanForm(request.POST, request.FILES, instance=laporan, dokumen=dokumen)
        if form.is_valid():
            form.save()
            dokumen.status = "Sudah Diunggah"  # ✅ Perbarui status dokumen
            dokumen.save()
            messages.success(request, "Laporan berhasil diperbarui!")
            return redirect("daftar_dokumen")
        else:
            messages.error(request, "Terjadi kesalahan. Periksa kembali data yang Anda masukkan.")
    else:
        form = LaporanForm(instance=laporan, dokumen=dokumen)

    return render(request, "dokumen/unggah_laporan.html", {"form": form, "dokumen": dokumen})

# ✅ MENAMPILKAN DAFTAR DOKUMEN (DENGAN PAGINASI & PENCARIAN)
def daftar_dokumen(request):
    """Menampilkan daftar dokumen dengan pencarian & paginasi."""
    nomor_surat_query = request.GET.get("nomor_surat", "")
    tanggal_surat_query = request.GET.get("tanggal_surat", "")
    irban_query = request.GET.get("irban", "")

    # Filter pencarian
    dokumen_list = Dokumen.objects.select_related("laporan").all()
    
    if nomor_surat_query:
        dokumen_list = dokumen_list.filter(nomor_surat__icontains=nomor_surat_query)
    if tanggal_surat_query:
        dokumen_list = dokumen_list.filter(tanggal_surat=tanggal_surat_query)
    if irban_query:
        dokumen_list = dokumen_list.filter(irban__icontains=irban_query)  # ✅ Perbaiki pencarian irban

    # 🔹 Urutkan dokumen terbaru ke atas
    dokumen_list = dokumen_list.order_by("-tanggal_surat", "-id")

    # 🔹 PAGINASI: Batasi hanya 10 dokumen per halaman
    paginator = Paginator(dokumen_list, 10)
    page_number = request.GET.get("page")

    try:
        dokumen_page = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        dokumen_page = paginator.page(1)  # Jika error, kembali ke halaman pertama

    return render(request, "dokumen/daftar_dokumen.html", {"dokumen_list": dokumen_page})

# ✅ MENAMPILKAN DETAIL DOKUMEN
@login_required
def detail_dokumen(request, dokumen_id):
    dokumen = get_object_or_404(Dokumen, pk=dokumen_id)
    laporan = Laporan.objects.filter(dokumen=dokumen).first()  # Jika laporan ada

    print("Tim Audit yang dikirim ke template:", dokumen.tim_audit)  # Debugging

    # Cek dari mana user datang
    next_page = request.GET.get("next", request.META.get("HTTP_REFERER", "/"))

    return render(request, "dokumen/detail_dokumen.html", {
        "dokumen": dokumen,
        "laporan": laporan,
        "next_page": next_page,  # Kirim ke template
    })

# ✅ MENGUNDUH SURAT TUGAS
def unduh_surat_tugas(request, dokumen_id):
    """Mengunduh file surat tugas."""
    dokumen = get_object_or_404(Dokumen, id=dokumen_id)

    if not dokumen.file or not dokumen.file.name:
        messages.error(request, "File Surat Tugas tidak tersedia.")
        return redirect("daftar_dokumen")

    return FileResponse(dokumen.file.open("rb"), as_attachment=True)

# ✅ MENGUNDUH LAPORAN
def unduh_laporan(request, laporan_id):
    """Mengunduh file laporan."""
    laporan = get_object_or_404(Laporan, id=laporan_id)

    if not laporan.file or not laporan.file.name:
        messages.error(request, "File Laporan tidak tersedia.")
        return redirect("daftar_dokumen")

    return FileResponse(laporan.file.open("rb"), as_attachment=True)

import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import now, timedelta
from .models import Dokumen, Laporan  # Pastikan model Laporan diimpor jika ada

def ekspor_excel(request, rentang):
    # Hitung rentang waktu
    today = now().date()
    if rentang == "minggu":
        start_date = today - timedelta(days=7)
    elif rentang == "bulan":
        start_date = today - timedelta(days=30)
    elif rentang == "tahun":
        start_date = today - timedelta(days=365)
    else:
        return HttpResponse("Rentang waktu tidak valid.", status=400)

    # Ambil dokumen yang memiliki Surat Tugas dan Laporan dalam rentang waktu tertentu
    dokumen_list = Dokumen.objects.filter(
        tanggal_surat__gte=start_date,
        file__isnull=False,
        laporan__file__isnull=False
    )

    if not dokumen_list.exists():
        return HttpResponse("Tidak ada dokumen yang memenuhi kriteria.", status=404)

    # Buat DataFrame Pandas
    data = []
    for dokumen in dokumen_list:
        laporan = Laporan.objects.filter(dokumen=dokumen).first()

        # Konversi Tim Audit dari list ke string yang mudah dibaca
        if isinstance(dokumen.tim_audit, list):  # Jika tersimpan sebagai list
            tim_audit_str = ", ".join([f"{t['nama']} - {t['jabatan']}" for t in dokumen.tim_audit])
        else:
            tim_audit_str = str(dokumen.tim_audit)  # Jika bukan list, langsung ubah ke string

        data.append({
            "Nomor Surat": dokumen.nomor_surat,
            "Tanggal Surat": dokumen.tanggal_surat.strftime("%d-%m-%Y"),
            "Irban": dokumen.irban,
            "Tim Audit": tim_audit_str,  # ✅ Perbaikan disini
            "Uraian": dokumen.uraian,
            "Nomor Laporan": laporan.nomor_laporan if laporan else "-",
            "Tanggal Laporan": laporan.tanggal_laporan.strftime("%d-%m-%Y") if laporan else "-",
            "Keterangan": laporan.keterangan if laporan else "-",
        })

    df = pd.DataFrame(data)

    # Simpan ke response sebagai file Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="dokumen_{rentang}.xlsx"'

    with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Dokumen", index=False)

    return response

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Dokumen  # Pastikan model Dokumen sudah di-import

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:  # Superuser & Admin ke admin_dashboard
                return redirect('admin_dashboard')
            else:  # Pengguna biasa ke dashboard
                return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah!")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profil(request):
    user = request.user
    return render(request, 'profil.html', {'user': user})

@login_required(login_url='login')
def dashboard(request):
    dokumen_list = Dokumen.objects.filter(pengirim=request.user)
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard')  # Cegah akses jika bukan admin

    users = User.objects.all()
    dokumen_list = Dokumen.objects.all() 
    return render(request, 'admin_dashboard.html', {'users': users})

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username sudah digunakan.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email sudah digunakan.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Pendaftaran berhasil! Silakan login.")
                return redirect('login')
        else:
            messages.error(request, "Password tidak cocok.")

    return render(request, 'register.html')

# Cek apakah user adalah admin
def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def hapus_pengguna(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "Pengguna berhasil dihapus.")
    return redirect('admin_dashboard')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='dashboard')
def create_user(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        is_staff = request.POST.get('is_staff', False) == "on"  # Checkbox untuk admin

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff  # Tandai sebagai admin jika dipilih
            user.save()
            messages.success(request, "Akun berhasil dibuat!")
            return redirect('admin_dashboard')

    return render(request, 'dokumen/create_user.html')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='dashboard')
def update_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        full_name = request.POST['full_name']
        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = request.POST.get('is_staff', False) == "on"

        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])

        user.save()
        messages.success(request, "Akun berhasil diperbarui!")
        return redirect('admin_dashboard')

    return render(request, 'dokumen/update_user.html', {'user': user})

def daftar_dokumen_admin(request):

    nomor_surat_query = request.GET.get("nomor_surat", "")
    tanggal_surat_query = request.GET.get("tanggal_surat", "")
    irban_query = request.GET.get("irban", "")

    # Filter pencarian
    dokumen_list = Dokumen.objects.select_related("user", "laporan").all()
    
    if nomor_surat_query:
        dokumen_list = dokumen_list.filter(nomor_surat__icontains=nomor_surat_query)
    if tanggal_surat_query:
        dokumen_list = dokumen_list.filter(tanggal_surat=tanggal_surat_query)
    if irban_query:
        dokumen_list = dokumen_list.filter(irban__icontains=irban_query)  # ✅ Perbaiki pencarian irban

    # 🔹 Urutkan dokumen terbaru ke atas
    dokumen_list = dokumen_list.order_by("-tanggal_surat", "-id")

    # 🔹 PAGINASI: Batasi hanya 10 dokumen per halaman
    paginator = Paginator(dokumen_list, 10)
    page_number = request.GET.get("page")

    try:
        dokumen_page = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        dokumen_page = paginator.page(1)  # Jika error, kembali ke halaman pertama

    return render(request, 'dokumen/daftar_dokumen_admin.html', {'dokumen_list': dokumen_list})

def hapus_surat_tugas(request, dokumen_id):
    dokumen = get_object_or_404(Dokumen, id=dokumen_id)
    dokumen.delete()
    return redirect('daftar_dokumen_admin')

def hapus_laporan(request, laporan_id):
    laporan = get_object_or_404(Laporan, id=laporan_id)
    laporan.delete()
    return redirect('daftar_dokumen_admin')

@user_passes_test(is_admin)
def hapus_dokumen(request, dokumen_id):
    dokumen = get_object_or_404(Dokumen, id=dokumen_id)
    dokumen.delete()
    messages.success(request, "Dokumen berhasil dihapus.")
    return redirect('admin_dashboard')
