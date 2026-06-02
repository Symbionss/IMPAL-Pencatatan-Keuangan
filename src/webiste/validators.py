import re
from django.core.exceptions import ValidationError

def validate_password_policy(password, user=None):
    """
    Memvalidasi password sesuai dengan kebijakan keamanan modern.
    """
    # 1. Cek panjang minimum dan maksimum
    if len(password) < 8:
        raise ValidationError("Password minimal 8 karakter.")
    if len(password) > 64:
        raise ValidationError("Password maksimal 64 karakter.")
    
    # 2. Cek kombinasi karakter (kompleksitas)
    categories_matched = 0
    if re.search(r'[A-Z]', password):
        categories_matched += 1
    if re.search(r'[a-z]', password):
        categories_matched += 1
    if re.search(r'\d', password):
        categories_matched += 1
    if re.search(r'[^A-Za-z0-9]', password):
        categories_matched += 1
        
    if categories_matched < 3:
        raise ValidationError("Password harus mengandung minimal 3 dari 4 kategori: huruf besar, huruf kecil, angka, dan karakter khusus.")
        
    # 3. Cek riwayat password (jika pengguna sudah ada/update password)
    if user:
        from .models import PasswordHistory
        # Ambil 5 password terakhir dari riwayat
        recent_passwords = PasswordHistory.objects.filter(user=user).order_by('-created_at')[:5]
        for history in recent_passwords:
            # Peringatan: Saat ini sistem menggunakan perbandingan plaintext. 
            # Sangat direkomendasikan untuk menggunakan hashing (misal: make_password / check_password).
            if password == history.password_hash:
                raise ValidationError("Password tidak boleh sama dengan 5 password terakhir yang pernah digunakan.")
