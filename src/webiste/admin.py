from django.contrib import admin
from .models import User, Admin, UserBiasa, Kategori, Pemasukan, Pengeluaran, Anggaran

# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(UserBiasa)
admin.site.register(Kategori)
admin.site.register(Pemasukan)
admin.site.register(Pengeluaran)
admin.site.register(Anggaran)
