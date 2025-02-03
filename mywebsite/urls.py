from django.contrib import admin
from django.urls import path, include
from .views import register_view, profil
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', profil, name='profil'),
    path('dokumen/', include('dokumen.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

