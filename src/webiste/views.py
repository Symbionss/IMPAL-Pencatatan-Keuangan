from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from .models import User

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
        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()

        total_p = 0
        total_q = 0
        total_anggaran = 0
        pengeluaran_terbaru = []
        anggaran_bulanan = []
        if user_biasa:
            from django.db.models import Sum
            total_p = Pemasukan.objects.filter(id_user=user_biasa).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
            total_q = Pengeluaran.objects.filter(id_user=user_biasa).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
            pengeluaran_terbaru = Pengeluaran.objects.filter(id_user=user_biasa).order_by('-tanggal')[:4]

            # Anggaran calculation
            total_anggaran = Anggaran.objects.filter(id_user=user_biasa).aggregate(Sum('jumlah_anggaran'))['jumlah_anggaran__sum'] or 0
            all_anggarans = Anggaran.objects.filter(id_user=user_biasa)
            
            def format_rupiah_internal(val):
                return "{:,.0f}".format(val).replace(',', '.')
                
            for ang in all_anggarans:
                kat = ang.id_kategori
                terpakai = Pengeluaran.objects.filter(id_user=user_biasa, id_kategori=kat).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
                sisa = ang.jumlah_anggaran - terpakai
                anggaran_bulanan.append({
                    'kategori': kat.nama,
                    'anggaran': format_rupiah_internal(ang.jumlah_anggaran),
                    'terpakai': format_rupiah_internal(terpakai),
                    'sisa': format_rupiah_internal(sisa),
                    'icon': 'bx-briefcase-alt-2',
                    'color_class': 'blue-bg'
                })
            
        saldo = total_p - total_q
        
        def format_rupiah(value):
            return "{:,.0f}".format(value).replace(',', '.')

        context = {
            'nama': request.session.get('nama'),
            'total_pemasukan': format_rupiah(total_p),
            'total_pengeluaran': format_rupiah(total_q),
            'saldo_saat_ini': format_rupiah(saldo),
            'anggaran_bulan_ini': format_rupiah(total_anggaran),
            'pengeluaran_terbaru': pengeluaran_terbaru,
            'anggaran_bulanan': anggaran_bulanan
        }
        return render(request, self.template_name, context)

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(id_user=user_id).first()
            if user:
                user.logout()
                request.session.flush()
                return redirect('index')

from .models import User, UserBiasa, Admin, Kategori, Pemasukan

class PemasukanListView(TemplateView):
    template_name = "pemasukan.html"
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
            
        user_id = request.session.get('user_id')
        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            base_user = User.objects.filter(id_user=user_id).first()
            if base_user:
                try:
                    user_biasa = UserBiasa(user_ptr_id=base_user.id_user, nama=base_user.nama, password=base_user.password)
                    user_biasa.save()
                except Exception:
                    user_biasa = UserBiasa.objects.first()
                    
        # Load the user's pemasukan records if the user exists
        pemasukan_list = []
        if user_biasa:
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
        
        try:
            jumlah_float = float(jumlah)
        except ValueError:
            jumlah_float = 0.0

        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            base_user = User.objects.filter(id_user=user_id).first()
            if base_user:
                try:
                    user_biasa = UserBiasa(user_ptr_id=base_user.id_user, nama=base_user.nama, password=base_user.password)
                    user_biasa.save()
                except Exception:
                    user_biasa = UserBiasa.objects.first()
            if not user_biasa:
                user_biasa = UserBiasa.objects.create(nama="Dummy User Biasa", password="123")

        admin_user = Admin.objects.first()
        if not admin_user:
            admin_user = Admin.objects.create(nama="System Admin", password="admin")
            
        kategori = Kategori.objects.filter(nama__iexact=kategori_nama).first()
        if not kategori and kategori_nama:
            if admin_user:
                kategori = Kategori.objects.create(
                    nama=kategori_nama,
                    tipe_kategori="Pemasukan",
                    id_user=admin_user
                )

        if not kategori:
            kategori = Kategori.objects.first()
            if not kategori:
                kategori = Kategori.objects.create(nama="Lainnya", tipe_kategori="Pemasukan", id_user=admin_user)

        if user_biasa and kategori and tanggal:
            Pemasukan.objects.create(
                jumlah=jumlah_float,
                tanggal=tanggal,
                deskripsi=deskripsi,
                id_user=user_biasa,
                id_kategori=kategori
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
        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            base_user = User.objects.filter(id_user=user_id).first()
            if base_user:
                try:
                    user_biasa = UserBiasa(user_ptr_id=base_user.id_user, nama=base_user.nama, password=base_user.password)
                    user_biasa.save()
                except Exception:
                    user_biasa = UserBiasa.objects.first()
                    
        pengeluaran_list = []
        if user_biasa:
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
        
        try:
            jumlah_float = float(jumlah)
        except ValueError:
            jumlah_float = 0.0

        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            base_user = User.objects.filter(id_user=user_id).first()
            if base_user:
                try:
                    user_biasa = UserBiasa(user_ptr_id=base_user.id_user, nama=base_user.nama, password=base_user.password)
                    user_biasa.save()
                except Exception:
                    user_biasa = UserBiasa.objects.first()
            if not user_biasa:
                user_biasa = UserBiasa.objects.create(nama="Dummy User Biasa", password="123")

        admin_user = Admin.objects.first()
        if not admin_user:
            admin_user = Admin.objects.create(nama="System Admin", password="admin")
            
        kategori = Kategori.objects.filter(nama__iexact=kategori_nama).first()
        if not kategori and kategori_nama:
            if admin_user:
                kategori = Kategori.objects.create(
                    nama=kategori_nama,
                    tipe_kategori="Pengeluaran",
                    id_user=admin_user
                )

        if not kategori:
            kategori = Kategori.objects.first()
            if not kategori:
                kategori = Kategori.objects.create(nama="Lainnya", tipe_kategori="Pengeluaran", id_user=admin_user)

        if user_biasa and kategori and tanggal:
            Pengeluaran.objects.create(
                jumlah=jumlah_float,
                tanggal=tanggal,
                deskripsi=deskripsi,
                id_user=user_biasa,
                id_kategori=kategori
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
        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            base_user = User.objects.filter(id_user=user_id).first()
            if base_user:
                try:
                    user_biasa = UserBiasa(user_ptr_id=base_user.id_user, nama=base_user.nama, password=base_user.password)
                    user_biasa.save()
                except Exception:
                    user_biasa = UserBiasa.objects.first()
                    
        anggaran_list = []
        if user_biasa:
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
        
        try:
            jumlah_float = float(jumlah_anggaran)
        except ValueError:
            jumlah_float = 0.0

        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            base_user = User.objects.filter(id_user=user_id).first()
            if base_user:
                try:
                    user_biasa = UserBiasa(user_ptr_id=base_user.id_user, nama=base_user.nama, password=base_user.password)
                    user_biasa.save()
                except Exception:
                    user_biasa = UserBiasa.objects.first()
            if not user_biasa:
                user_biasa = UserBiasa.objects.create(nama="Dummy User Biasa", password="123")

        admin_user = Admin.objects.first()
        if not admin_user:
            admin_user = Admin.objects.create(nama="System Admin", password="admin")
            
        kategori = Kategori.objects.filter(nama__iexact=kategori_nama).first()
        if not kategori and kategori_nama:
            if admin_user:
                kategori = Kategori.objects.create(
                    nama=kategori_nama,
                    tipe_kategori="Anggaran",
                    id_user=admin_user
                )

        if not kategori:
            kategori = Kategori.objects.first()
            if not kategori:
                kategori = Kategori.objects.create(nama="Lainnya", tipe_kategori="Anggaran", id_user=admin_user)

        if user_biasa and kategori and periode:
            Anggaran.objects.create(
                jumlah_anggaran=jumlah_float,
                periode=periode,
                id_user=user_biasa,
                id_kategori=kategori
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

        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            user_biasa = UserBiasa.objects.first()

        admin_user = Admin.objects.first()
        if not admin_user:
            admin_user = Admin.objects.create(nama="System Admin", password="admin")

        kategori = Kategori.objects.filter(nama__iexact=kategori_nama).first()
        if not kategori:
            kategori = Kategori.objects.create(nama=kategori_nama, tipe_kategori="Pemasukan", id_user=admin_user)

        if user_biasa and tanggal:
            pemasukan = Pemasukan.objects.create(
                jumlah=jumlah,
                tanggal=tanggal,
                deskripsi=deskripsi,
                id_user=user_biasa,
                id_kategori=kategori
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

        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            user_biasa = UserBiasa.objects.first()

        admin_user = Admin.objects.first()
        if not admin_user:
            admin_user = Admin.objects.create(nama="System Admin", password="admin")

        kategori = Kategori.objects.filter(nama__iexact=kategori_nama).first()
        if not kategori:
            kategori = Kategori.objects.create(nama=kategori_nama, tipe_kategori="Pengeluaran", id_user=admin_user)

        if user_biasa and tanggal:
            pengeluaran = Pengeluaran.objects.create(
                jumlah=jumlah,
                tanggal=tanggal,
                deskripsi=deskripsi,
                id_user=user_biasa,
                id_kategori=kategori
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

        user_biasa = UserBiasa.objects.filter(id_user=user_id).first()
        if not user_biasa:
            user_biasa = UserBiasa.objects.first()

        admin_user = Admin.objects.first()
        if not admin_user:
            admin_user = Admin.objects.create(nama="System Admin", password="admin")

        kategori = Kategori.objects.filter(nama__iexact=kategori_nama).first()
        if not kategori:
            kategori = Kategori.objects.create(nama=kategori_nama, tipe_kategori="Anggaran", id_user=admin_user)

        if user_biasa and periode:
            anggaran = Anggaran.objects.create(
                jumlah_anggaran=jumlah,
                periode=periode,
                id_user=user_biasa,
                id_kategori=kategori
            )
            return JsonResponse({'status': 'success', 'message': 'Anggaran created', 'id': anggaran.id_anggaran})
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

