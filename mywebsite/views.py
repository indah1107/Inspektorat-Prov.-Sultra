from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from dokumen.models import Dokumen


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:  
                return redirect('admin_dashboard')
            else:  
                return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah!")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profil(request):
    user = request.user
    return render(request, 'profil.html', {'user': user})

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='dashboard')
def profil_admin(request):
    return render(request, 'profil_admin.html', {'user': request.user})

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
                user.save()  

                messages.success(request, "Pendaftaran berhasil! Silakan login.")
                return redirect('login')
        else:
            messages.error(request, "Password tidak cocok.")

    return render(request, 'register.html')

@login_required
def profil(request):
    user = request.user
    return render(request, 'profil.html', {'user': user, 'full_name': user.get_full_name()})

@login_required(login_url='login')
def dashboard(request):
    dokumen_belum_diunggah = Dokumen.objects.filter(laporan_diunggah=False)
    return render(request, 'dashboard.html', {"dokumen_belum_diunggah": dokumen_belum_diunggah})


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='dashboard')
def admin_dashboard(request):
    dokumen_belum_diunggah = Dokumen.objects.filter(laporan_diunggah=False)
    print(f"Jumlah dokumen yang belum diunggah: {dokumen_belum_diunggah.count()}")  # Tambahkan baris ini untuk debugging
    if not request.user.is_staff:
        return redirect('dashboard') 

    users_list = User.objects.all().order_by('-is_staff') 
    paginator = Paginator(users_list, 10)

    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, 'admin_dashboard.html', {'users': users, 'dokumen_belum_diunggah': dokumen_belum_diunggah})

