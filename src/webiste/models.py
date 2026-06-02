from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import render, redirect

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    @classmethod
    def login(cls, input_nama, input_password):
        # verifikasi database
        user_valid = cls.objects.filter(nama=input_nama, password=input_password).first()

        if user_valid:
            return user_valid
        else:
            return None

    @classmethod
    def logout(cls, user_id):
        user_valid = cls.objects.filter(id_user=user_id).first()
        if user_valid:
            return user_valid
        else:
            return None

    def __str__(self):
        return self.nama

class Admin(User):
    @classmethod
    def get_system_admin(cls):
        admin_user = cls.objects.first()
        if not admin_user:
            admin_user = cls.objects.create(nama="System Admin", password="admin")
        return admin_user

    def tambahKategori(self, nama: str, tipe: str):
        kategori = Kategori.objects.filter(nama__iexact=nama).first()
        if not kategori:
            kategori = Kategori.objects.create(
                nama=nama,
                tipe_kategori=tipe,
                id_user=self
            )
        return kategori

    def editKategori(self, id_kategori: int, nama_baru: str) -> None:
        kategori = Kategori.objects.filter(id_kategori=id_kategori).first()
        if kategori:
            kategori.nama = nama_baru
            kategori.simpan()

    def hapusKategori(self, id_kategori: int) -> None:
        kategori = Kategori.objects.filter(id_kategori=id_kategori).first()
        if kategori:
            kategori.hapus()

class UserBiasa(User):
    @classmethod
    def get_or_create_user(cls, user_id):
        user_biasa = cls.objects.filter(id_user=user_id).first()
        if not user_biasa:
            base_user = User.objects.filter(id_user=user_id).first()
            if base_user:
                try:
                    user_biasa = cls(user_ptr_id=base_user.id_user, nama=base_user.nama, password=base_user.password)
                    user_biasa.save()
                except Exception:
                    user_biasa = cls.objects.first()
            if not user_biasa:
                user_biasa = cls.objects.create(nama="Dummy User Biasa", password="123")
        return user_biasa

    def tambahPemasukan(self, jumlah, tanggal, deskripsi, kategori_nama):
        admin_user = Admin.get_system_admin()
        kategori = admin_user.tambahKategori(nama=kategori_nama or "Lainnya", tipe="Pemasukan")
        pemasukan = Pemasukan(
            jumlah=float(jumlah or 0),
            tanggal=tanggal,
            deskripsi=deskripsi,
            id_user=self,
            id_kategori=kategori
        )
        pemasukan.simpan()
        return pemasukan

    def tambahPengeluaran(self, jumlah, tanggal, deskripsi, kategori_nama):
        admin_user = Admin.get_system_admin()
        kategori = admin_user.tambahKategori(nama=kategori_nama or "Lainnya", tipe="Pengeluaran")
        pengeluaran = Pengeluaran(
            jumlah=float(jumlah or 0),
            tanggal=tanggal,
            deskripsi=deskripsi,
            id_user=self,
            id_kategori=kategori
        )
        pengeluaran.simpan()
        return pengeluaran

    def setAnggaran(self, jumlah_anggaran, periode, kategori_nama):
        admin_user = Admin.get_system_admin()
        kategori = admin_user.tambahKategori(nama=kategori_nama or "Lainnya", tipe="Anggaran")
        anggaran = Anggaran(
            jumlah_anggaran=float(jumlah_anggaran or 0),
            periode=periode,
            id_user=self,
            id_kategori=kategori
        )
        anggaran.simpan()
        return anggaran

    def lihatLaporan(self) -> dict:
        total_p = Pemasukan.getTotal(self)
        total_q = Pengeluaran.getTotal(self)
        saldo = total_p - total_q
        
        from django.db.models import Sum
        total_anggaran = Anggaran.objects.filter(id_user=self).aggregate(Sum('jumlah_anggaran'))['jumlah_anggaran__sum'] or 0
        
        pengeluaran_terbaru = Pengeluaran.objects.filter(id_user=self).order_by('-tanggal')[:4]
        
        all_anggarans = Anggaran.objects.filter(id_user=self)
        anggaran_bulanan = []
        
        def format_rupiah_internal(val):
            return "{:,.0f}".format(val).replace(',', '.')
            
        for ang in all_anggarans:
            kat = ang.id_kategori
            terpakai = Pengeluaran.objects.filter(id_user=self, id_kategori=kat).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
            sisa = ang.jumlah_anggaran - terpakai
            anggaran_bulanan.append({
                'kategori': kat.nama,
                'anggaran': format_rupiah_internal(ang.jumlah_anggaran),
                'terpakai': format_rupiah_internal(terpakai),
                'sisa': format_rupiah_internal(sisa),
                'icon': 'bx-briefcase-alt-2',
                'color_class': 'blue-bg'
            })
            
        return {
            'total_pemasukan': total_p,
            'total_pengeluaran': total_q,
            'saldo_saat_ini': saldo,
            'anggaran_bulan_ini': total_anggaran,
            'pengeluaran_terbaru': pengeluaran_terbaru,
            'anggaran_bulanan': anggaran_bulanan
        }

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    tipe_kategori = models.CharField(max_length=255)
    id_user = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column="id_user")

    def __str__(self):
        return self.nama

    def simpan(self) -> None:
        self.save()

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def hapus(self) -> None:
        self.delete()

class Pemasukan(models.Model):
    id_pemasukan = models.AutoField(primary_key=True)
    jumlah = models.FloatField()
    tanggal = models.DateField()
    deskripsi = models.CharField(max_length=255)
    id_user = models.ForeignKey(UserBiasa, on_delete=models.CASCADE, db_column="id_user")
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, db_column="id_kategori")

    def __str__(self):
        return self.deskripsi

    def simpan(self) -> None:
        self.save()

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def hapus(self) -> None:
        self.delete()

    @classmethod
    def getTotal(cls, user) -> float:
        from django.db.models import Sum
        return cls.objects.filter(id_user=user).aggregate(Sum('jumlah'))['jumlah__sum'] or 0.0

class Pengeluaran(models.Model):
    id_pengeluaran = models.AutoField(primary_key=True)
    jumlah = models.FloatField()
    tanggal = models.DateField()
    deskripsi = models.CharField(max_length=255)
    id_user = models.ForeignKey(UserBiasa, on_delete=models.CASCADE, db_column="id_user")
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, db_column="id_kategori")

    def __str__(self):
        return self.deskripsi

    def simpan(self) -> None:
        self.save()

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def hapus(self) -> None:
        self.delete()

    @classmethod
    def getTotal(cls, user) -> float:
        from django.db.models import Sum
        return cls.objects.filter(id_user=user).aggregate(Sum('jumlah'))['jumlah__sum'] or 0.0

class Anggaran(models.Model):
    id_anggaran = models.AutoField(primary_key=True)
    jumlah_anggaran = models.FloatField()
    periode = models.CharField(max_length=255)
    id_user = models.ForeignKey(UserBiasa, on_delete=models.CASCADE, db_column="id_user")
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, db_column="id_kategori")

    def __str__(self):
        return f"Anggaran {self.periode}"

    def simpan(self) -> None:
        self.save()

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def hapus(self) -> None:
        self.delete()

    def cekLimit(self, pengeluaran) -> bool:
        from django.db.models import Sum
        terpakai = Pengeluaran.objects.filter(id_user=self.id_user, id_kategori=self.id_kategori).aggregate(Sum('jumlah'))['jumlah__sum'] or 0
        return (terpakai + pengeluaran) > self.jumlah_anggaran

class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

