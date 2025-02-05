from django.contrib import admin
from django.urls import path, include
from .views import register_view, profil, login_view, logout_view, register_view, dashboard, admin_dashboard
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profil/', profil, name='profil'),
    path('profil_admin/', views.profil_admin, name='profil_admin'),
    path('dokumen/', include('dokumen.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

