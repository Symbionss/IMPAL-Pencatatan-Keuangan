"""cfehome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webiste.views import (
    IndexView, DashboardView, LogoutView, 
    PemasukanListView, AddPemasukanView, 
    PengeluaranListView, AddPengeluaranView, 
    AnggaranListView, AddAnggaranView,
    RegisterView,
    UserLoginAPIView, PemasukanAPIView, PengeluaranAPIView, AnggaranAPIView,
    UserLogoutAPIView, LaporanAPIView,
    KategoriAPIView, KategoriDetailAPIView,
    PemasukanDetailAPIView, PengeluaranDetailAPIView, AnggaranDetailAPIView,
    PemasukanTotalAPIView, PengeluaranTotalAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('pemasukan/', PemasukanListView.as_view(), name='pemasukan'),
    path('pemasukan/add/', AddPemasukanView.as_view(), name='add_pemasukan'),
    path('pengeluaran/', PengeluaranListView.as_view(), name='pengeluaran'),
    path('pengeluaran/add/', AddPengeluaranView.as_view(), name='add_pengeluaran'),
    path('anggaran/', AnggaranListView.as_view(), name='anggaran'),
    path('anggaran/add/', AddAnggaranView.as_view(), name='add_anggaran'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # API endpoints untuk Postman
    path('api/login/', UserLoginAPIView.as_view(), name='api_login'),
    path('api/pemasukan/', PemasukanAPIView.as_view(), name='api_pemasukan'),
    path('api/pengeluaran/', PengeluaranAPIView.as_view(), name='api_pengeluaran'),
    path('api/anggaran/', AnggaranAPIView.as_view(), name='api_anggaran'),
    path('api/logout/', UserLogoutAPIView.as_view(), name='api_logout'),
    path('api/laporan/', LaporanAPIView.as_view(), name='api_laporan'),
    path('api/kategori/', KategoriAPIView.as_view(), name='api_kategori'),
    path('api/kategori/<int:pk>/', KategoriDetailAPIView.as_view(), name='api_kategori_detail'),
    path('api/pemasukan/total/', PemasukanTotalAPIView.as_view(), name='api_pemasukan_total'),
    path('api/pengeluaran/total/', PengeluaranTotalAPIView.as_view(), name='api_pengeluaran_total'),
    path('api/pemasukan/<int:pk>/', PemasukanDetailAPIView.as_view(), name='api_pemasukan_detail'),
    path('api/pengeluaran/<int:pk>/', PengeluaranDetailAPIView.as_view(), name='api_pengeluaran_detail'),
    path('api/anggaran/<int:pk>/', AnggaranDetailAPIView.as_view(), name='api_anggaran_detail'),
]
