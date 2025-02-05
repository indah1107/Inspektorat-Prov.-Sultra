from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:  # Jika admin, arahkan ke halaman admin
                return redirect('admin_dashboard')
            else:  # Jika pengguna biasa, arahkan ke dashboard
                return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah!")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required  # Pastikan hanya pengguna yang sudah login bisa mengakses profil
def profil(request):
    user = request.user  # Mengambil informasi pengguna yang sedang login
    return render(request, 'profil.html', {'user': user})

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='dashboard')  # Redirect jika bukan admin
def profil_admin(request):
    return render(request, 'profil_admin.html', {'user': request.user})

@login_required(login_url='login')
def dashboard(request):
    # dokumen_list = Dokumen.objects.filter(pengirim=request.user)
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')  # Cegah akses jika bukan admin

    # Ambil semua user untuk manajemen akun
    users = User.objects.all()
    # dokumen_list = Dokumen.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

def register_view(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

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
                user.first_name = first_name
                user.last_name = last_name
                user.save()  # Pastikan dipanggil setelah mengatur first_name dan last_name

                messages.success(request, "Pendaftaran berhasil! Silakan login.")
                return redirect('login')
        else:
            messages.error(request, "Password tidak cocok.")

    return render(request, 'register.html')

@login_required
def profil(request):
    user = request.user
    return render(request, 'profil.html', {'user': user, 'full_name': user.get_full_name()})
