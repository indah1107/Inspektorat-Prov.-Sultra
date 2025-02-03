from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    context ={
        'title':'Inspektorat',
        'headline':'Selamat datang di website Inspektorat',
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect ke dashboard jika berhasil login
        else:
            messages.error(request, "Username atau password salah!")

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')  # Arahkan kembali ke halaman login setelah logout

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate

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
                user.save()
                messages.success(request, "Pendaftaran berhasil! Silakan login.")
                return redirect('login')
        else:
            messages.error(request, "Password tidak cocok.")

    return render(request, 'register.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        # Ambil data dari form
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validasi apakah password dan konfirmasi password sama
        if password != confirm_password:
            messages.error(request, 'Password dan konfirmasi password tidak cocok')
            return redirect('register')

        # Buat akun pengguna baru
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = fullname
        user.save()

        messages.success(request, 'Akun berhasil dibuat. Silakan login.')
        return redirect('login')  # Redirect ke halaman login setelah pendaftaran berhasil
    return render(request, 'register.html')

from django.contrib.auth.decorators import login_required

@login_required  # Pastikan pengguna yang login dapat mengakses halaman profil
def profil(request):
    user = request.user  # Ambil informasi pengguna yang sedang login
    return render(request, 'profil.html', {'user': user})