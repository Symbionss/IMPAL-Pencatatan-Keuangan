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

    def logout(self) -> None:
        return None

    def __str__(self):
        return self.nama

class Admin(User):
    def tambahKategori(self, nama: str, tipe: str) -> None:
        pass

    def editKategori(self, id_kategori: int) -> None:
        pass

    def hapusKategori(self, id_kategori: int) -> None:
        pass

class UserBiasa(User):
    def tambahPemasukan(self, data) -> None:
        pass

    def tambahPengeluaran(self, data) -> None:
        pass

    def setAnggaran(self, data) -> None:
        pass

    def lihatLaporan(self) -> str:
        return ""

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=255)
    tipe_kategori = models.CharField(max_length=255)
    id_user = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column="id_user")

    def __str__(self):
        return self.nama

    def simpan(self) -> None:
        pass

    def update(self) -> None:
        pass

    def hapus(self) -> None:
        pass

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
        pass

    def update(self) -> None:
        pass

    def hapus(self) -> None:
        pass

    def getTotal(self) -> float:
        return 0.0

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
        pass

    def update(self) -> None:
        pass

    def hapus(self) -> None:
        pass

    def getTotal(self) -> float:
        return 0.0

class Anggaran(models.Model):
    id_anggaran = models.AutoField(primary_key=True)
    jumlah_anggaran = models.FloatField()
    periode = models.CharField(max_length=255)
    id_user = models.ForeignKey(UserBiasa, on_delete=models.CASCADE, db_column="id_user")
    id_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, db_column="id_kategori")

    def __str__(self):
        return f"Anggaran {self.periode}"

    def simpan(self) -> None:
        pass

    def update(self) -> None:
        pass

    def hapus(self) -> None:
        pass

    def cekLimit(self, pengeluaran) -> bool:
        return True


