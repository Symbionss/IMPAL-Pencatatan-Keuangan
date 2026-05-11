from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from .models import User

class RegisterView(TemplateView):
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        nama = request.POST.get('nama')
        password = request.POST.get('password')
        retype_password = request.POST.get('retype-password')

        if nama and password and retype_password:
            if password == retype_password:
                User.objects.create(
                    nama=nama,
                    password=password
                )
                return redirect('index')
            else:
                messages.error(request, "Password yang dimasukan tidak sama.")
                return render(request, self.template_name)
        else:
            messages.error(request, "Tolong isi nama, password, dan retype password.")
            return render(request, self.template_name)

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        # Jika sudah login, langsung ke dashboard
        if request.session.get('user_id'):
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nama = request.POST.get('nama')
        password = request.POST.get('password')
        
        if nama and password:
            user = User.login(input_nama=nama, input_password=password)
            if user:
                # Simpan id dan nama ke sesi
                request.session['user_id'] = user.id_user
                request.session['nama'] = user.nama
                return redirect('dashboard')
            else:
                messages.error(request, "Nama atau password tidak tepat.")
        else:
            messages.error(request, "Mohon isi nama dan password.")
                
        return redirect('index')

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')

        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.get_or_create_user(user_id)

        laporan = user_biasa.lihatLaporan()
        
        def format_rupiah(value):
            return "{:,.0f}".format(value).replace(',', '.')

        context = {
            'nama': request.session.get('nama'),
            'total_pemasukan': format_rupiah(laporan['total_pemasukan']),
            'total_pengeluaran': format_rupiah(laporan['total_pengeluaran']),
            'saldo_saat_ini': format_rupiah(laporan['saldo_saat_ini']),
            'anggaran_bulan_ini': format_rupiah(laporan['anggaran_bulan_ini']),
            'pengeluaran_terbaru': laporan['pengeluaran_terbaru'],
            'anggaran_bulanan': laporan['anggaran_bulanan']
        }
        return render(request, self.template_name, context)

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.logout(user_id=user_id)
            if user:
                request.session.flush()
        return redirect('index')

from .models import User, UserBiasa, Admin, Kategori, Pemasukan

class PemasukanListView(TemplateView):
    template_name = "pemasukan.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
            
        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.get_or_create_user(user_id)
                    
        pemasukan_list = Pemasukan.objects.filter(id_user=user_biasa).order_by('-tanggal')
            
        context = {
            'nama': request.session.get('nama'),
            'pemasukan_list': pemasukan_list
        }
        return render(request, self.template_name, context)

class AddPemasukanView(TemplateView):
    template_name = "add_pemasukan.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
        context = {'nama': request.session.get('nama')}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')

        jumlah = request.POST.get('jumlah', '0')
        deskripsi = request.POST.get('deskripsi', '')
        kategori_nama = request.POST.get('kategori', '')
        tanggal = request.POST.get('tanggal')

        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.get_or_create_user(user_id)

        if tanggal:
            user_biasa.tambahPemasukan(
                jumlah=jumlah,
                tanggal=tanggal,
                deskripsi=deskripsi,
                kategori_nama=kategori_nama
            )
            return redirect('pemasukan')
            
        return redirect('add_pemasukan')

from .models import Pengeluaran

class PengeluaranListView(TemplateView):
    template_name = "pengeluaran.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
            
        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.get_or_create_user(user_id)
                    
        pengeluaran_list = Pengeluaran.objects.filter(id_user=user_biasa).order_by('-tanggal')
            
        context = {
            'nama': request.session.get('nama'),
            'pengeluaran_list': pengeluaran_list
        }
        return render(request, self.template_name, context)

class AddPengeluaranView(TemplateView):
    template_name = "add_pengeluaran.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
        context = {'nama': request.session.get('nama')}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')

        jumlah = request.POST.get('jumlah', '0')
        deskripsi = request.POST.get('deskripsi', '')
        kategori_nama = request.POST.get('kategori', '')
        tanggal = request.POST.get('tanggal')

        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.get_or_create_user(user_id)

        if tanggal:
            user_biasa.tambahPengeluaran(
                jumlah=jumlah,
                tanggal=tanggal,
                deskripsi=deskripsi,
                kategori_nama=kategori_nama
            )
            return redirect('pengeluaran')
            
        return redirect('add_pengeluaran')

from .models import Anggaran

class AnggaranListView(TemplateView):
    template_name = "anggaran.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
            
        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.get_or_create_user(user_id)
                    
        anggaran_list = Anggaran.objects.filter(id_user=user_biasa).order_by('-id_anggaran')
            
        context = {
            'nama': request.session.get('nama'),
            'anggaran_list': anggaran_list
        }
        return render(request, self.template_name, context)

class AddAnggaranView(TemplateView):
    template_name = "add_anggaran.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
        context = {'nama': request.session.get('nama')}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')

        jumlah_anggaran = request.POST.get('jumlah_anggaran', '0')
        periode = request.POST.get('periode', '')
        kategori_nama = request.POST.get('kategori', '')

        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.get_or_create_user(user_id)

        if periode:
            user_biasa.setAnggaran(
                jumlah_anggaran=jumlah_anggaran,
                periode=periode,
                kategori_nama=kategori_nama
            )
            return redirect('anggaran')
            
        return redirect('add_anggaran')

# =========================================================
# API VIEWS FOR POSTMAN TESTING
# =========================================================
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nama = data.get('nama')
            password = data.get('password')
        except:
            nama = request.POST.get('nama')
            password = request.POST.get('password')

        user = User.login(input_nama=nama, input_password=password)
        if user:
            return JsonResponse({'status': 'success', 'message': 'Login successful', 'user_id': user.id_user, 'nama': user.nama})
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)

@method_decorator(csrf_exempt, name='dispatch')
class PemasukanAPIView(View):
    def get(self, request, *args, **kwargs):
        pemasukan = Pemasukan.objects.all().values('id_pemasukan', 'jumlah', 'tanggal', 'deskripsi', 'id_kategori__nama', 'id_user__nama')
        return JsonResponse({'status': 'success', 'data': list(pemasukan)})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            jumlah = float(data.get('jumlah', 0))
            deskripsi = data.get('deskripsi', '')
            kategori_nama = data.get('kategori', 'Lainnya')
            tanggal = data.get('tanggal')
            user_id = data.get('user_id')
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        user_biasa = UserBiasa.get_or_create_user(user_id)

        if tanggal:
            pemasukan = user_biasa.tambahPemasukan(
                jumlah=jumlah,
                tanggal=tanggal,
                deskripsi=deskripsi,
                kategori_nama=kategori_nama
            )
            return JsonResponse({'status': 'success', 'message': 'Pemasukan created', 'id': pemasukan.id_pemasukan})
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PengeluaranAPIView(View):
    def get(self, request, *args, **kwargs):
        pengeluaran = Pengeluaran.objects.all().values('id_pengeluaran', 'jumlah', 'tanggal', 'deskripsi', 'id_kategori__nama', 'id_user__nama')
        return JsonResponse({'status': 'success', 'data': list(pengeluaran)})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            jumlah = float(data.get('jumlah', 0))
            deskripsi = data.get('deskripsi', '')
            kategori_nama = data.get('kategori', 'Lainnya')
            tanggal = data.get('tanggal')
            user_id = data.get('user_id')
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        user_biasa = UserBiasa.get_or_create_user(user_id)

        if tanggal:
            pengeluaran = user_biasa.tambahPengeluaran(
                jumlah=jumlah,
                tanggal=tanggal,
                deskripsi=deskripsi,
                kategori_nama=kategori_nama
            )
            return JsonResponse({'status': 'success', 'message': 'Pengeluaran created', 'id': pengeluaran.id_pengeluaran})
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class AnggaranAPIView(View):
    def get(self, request, *args, **kwargs):
        anggaran = Anggaran.objects.all().values('id_anggaran', 'jumlah_anggaran', 'periode', 'id_kategori__nama', 'id_user__nama')
        return JsonResponse({'status': 'success', 'data': list(anggaran)})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            jumlah = float(data.get('jumlah_anggaran', 0))
            periode = data.get('periode', '')
            kategori_nama = data.get('kategori', 'Lainnya')
            user_id = data.get('user_id')
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        user_biasa = UserBiasa.get_or_create_user(user_id)

        if periode:
            anggaran = user_biasa.setAnggaran(
                jumlah_anggaran=jumlah,
                periode=periode,
                kategori_nama=kategori_nama
            )
            return JsonResponse({'status': 'success', 'message': 'Anggaran created', 'id': anggaran.id_anggaran})
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
        except:
            user_id = request.POST.get('user_id')
        user = User.logout(user_id=user_id)
        if user:
            return JsonResponse({'status': 'success', 'message': 'Logout successful'})
        return JsonResponse({'status': 'error', 'message': 'Invalid user_id'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LaporanAPIView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'Missing user_id parameter'}, status=400)
        user_biasa = UserBiasa.get_or_create_user(user_id)
        laporan = user_biasa.lihatLaporan()
        if 'pengeluaran_terbaru' in laporan:
            laporan['pengeluaran_terbaru'] = list(laporan['pengeluaran_terbaru'].values('id_pengeluaran', 'jumlah', 'tanggal', 'deskripsi', 'id_kategori__nama'))
        return JsonResponse({'status': 'success', 'data': laporan})

@method_decorator(csrf_exempt, name='dispatch')
class KategoriAPIView(View):
    def get(self, request, *args, **kwargs):
        kategori = Kategori.objects.all().values()
        return JsonResponse({'status': 'success', 'data': list(kategori)})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nama = data.get('nama')
            tipe = data.get('tipe')
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        admin = Admin.get_system_admin()
        kategori = admin.tambahKategori(nama=nama, tipe=tipe)
        return JsonResponse({'status': 'success', 'message': 'Kategori created', 'id': kategori.id_kategori})

@method_decorator(csrf_exempt, name='dispatch')
class KategoriDetailAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        kategori = Kategori.objects.filter(id_kategori=pk).values().first()
        if kategori:
            return JsonResponse({'status': 'success', 'data': kategori})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)
    def put(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nama = data.get('nama')
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        admin = Admin.get_system_admin()
        admin.editKategori(id_kategori=pk, nama_baru=nama)
        return JsonResponse({'status': 'success', 'message': 'Kategori updated'})

    def delete(self, request, pk, *args, **kwargs):
        admin = Admin.get_system_admin()
        admin.hapusKategori(id_kategori=pk)
        return JsonResponse({'status': 'success', 'message': 'Kategori deleted'})

@method_decorator(csrf_exempt, name='dispatch')
class PemasukanDetailAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        pemasukan = Pemasukan.objects.filter(id_pemasukan=pk).values('id_pemasukan', 'jumlah', 'tanggal', 'deskripsi', 'id_kategori__nama', 'id_user__nama').first()
        if pemasukan:
            return JsonResponse({'status': 'success', 'data': pemasukan})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)
    def put(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        pemasukan = Pemasukan.objects.filter(id_pemasukan=pk).first()
        if pemasukan:
            pemasukan.update(**data)
            return JsonResponse({'status': 'success', 'message': 'Pemasukan updated'})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

    def delete(self, request, pk, *args, **kwargs):
        pemasukan = Pemasukan.objects.filter(id_pemasukan=pk).first()
        if pemasukan:
            pemasukan.hapus()
            return JsonResponse({'status': 'success', 'message': 'Pemasukan deleted'})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class PengeluaranDetailAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        pengeluaran = Pengeluaran.objects.filter(id_pengeluaran=pk).values('id_pengeluaran', 'jumlah', 'tanggal', 'deskripsi', 'id_kategori__nama', 'id_user__nama').first()
        if pengeluaran:
            return JsonResponse({'status': 'success', 'data': pengeluaran})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)
    def put(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        pengeluaran = Pengeluaran.objects.filter(id_pengeluaran=pk).first()
        if pengeluaran:
            pengeluaran.update(**data)
            return JsonResponse({'status': 'success', 'message': 'Pengeluaran updated'})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

    def delete(self, request, pk, *args, **kwargs):
        pengeluaran = Pengeluaran.objects.filter(id_pengeluaran=pk).first()
        if pengeluaran:
            pengeluaran.hapus()
            return JsonResponse({'status': 'success', 'message': 'Pengeluaran deleted'})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class AnggaranDetailAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        anggaran = Anggaran.objects.filter(id_anggaran=pk).values('id_anggaran', 'jumlah_anggaran', 'periode', 'id_kategori__nama', 'id_user__nama').first()
        if anggaran:
            return JsonResponse({'status': 'success', 'data': anggaran})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)
    def put(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        anggaran = Anggaran.objects.filter(id_anggaran=pk).first()
        if anggaran:
            anggaran.update(**data)
            return JsonResponse({'status': 'success', 'message': 'Anggaran updated'})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

    def delete(self, request, pk, *args, **kwargs):
        anggaran = Anggaran.objects.filter(id_anggaran=pk).first()
        if anggaran:
            anggaran.hapus()
            return JsonResponse({'status': 'success', 'message': 'Anggaran deleted'})
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class PemasukanTotalAPIView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'Missing user_id parameter'}, status=400)
        user_biasa = UserBiasa.get_or_create_user(user_id)
        total = Pemasukan.getTotal(user_biasa)
        return JsonResponse({'status': 'success', 'total': total})

@method_decorator(csrf_exempt, name='dispatch')
class PengeluaranTotalAPIView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'Missing user_id parameter'}, status=400)
        user_biasa = UserBiasa.get_or_create_user(user_id)
        total = Pengeluaran.getTotal(user_biasa)
        return JsonResponse({'status': 'success', 'total': total})
