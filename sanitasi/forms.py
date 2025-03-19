from django import forms
from .models import User
from datetime import date, datetime
import re

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="Password harus mengandung huruf, angka, dan karakter spesial."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Konfirmasi Password"
    )

    class Meta:
        model = User
        fields = [
            'username', 'nama', 'email', 'password', 'confirm_password', 
            'tanggal_lahir', 'nomor_hp', 'url_blog', 'deskripsi_diri', 'id_transaksi',
            'rating_ulasan'
        ]
        help_texts = {
            'username': "Hanya boleh mengandung huruf, angka, dan underscore (_).",
            'nama': "Nama hanya boleh berisi huruf, angka, -, . dan _ ",
            'email': "Pastikan email yang dimasukkan benar dan belum digunakan.",
            'tanggal_lahir': "Format: YYYY-MM-DD. Anda harus berusia minimal 12 tahun.",
            'nomor_hp': "Gunakan format internasional (contoh: +6281234567890) dengan 10-15 digit.",
            'url_blog': "Opsional. Masukkan URL blog dengan format yang benar (http/https).",
            'deskripsi_diri': "Maksimal 1000 karakter untuk mendeskripsikan diri Anda.",
            'id_transaksi': "mulai dengan huruf T-XXXXXXXXXX dengan X adalah angka"
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("Username hanya boleh mengandung huruf, angka, dan underscore.")
        return username

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        if not re.match(r'^[a-zA-Z0-9._-]+$', nama):
            raise forms.ValidationError("Nama hanya boleh berisi huruf, angka, -, . dan _ ")
        return nama

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email sudah digunakan oleh pengguna lain.")
        return email

    def clean_nomor_hp(self):
        nomor_hp = self.cleaned_data.get('nomor_hp')
        if not re.match(r'^\+\d{8,15}$', nomor_hp):
            raise forms.ValidationError("Nomor HP harus mengandung 10-15 digit dan bisa diawali dengan '+'.")
        return nomor_hp

    def clean_url_blog(self):
        url_blog = self.cleaned_data.get('url_blog')
        if url_blog and not re.match(r'^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$', url_blog):
            raise forms.ValidationError("URL blog tidak valid. Gunakan format yang benar.")
        return url_blog

    def clean_tanggal_lahir(self):
        tanggal_lahir = self.cleaned_data.get("tanggal_lahir")



        # Check minimum age (12 years old)
        today = date.today()
        min_birth_date = today.replace(year=today.year - 12)  # 12 years ago
        if tanggal_lahir > min_birth_date:
            raise forms.ValidationError("Anda harus berusia minimal 12 tahun.")

        return tanggal_lahir

    def clean_id_transaksi(self):
        id_transaksi = self.cleaned_data.get("id_transaksi")

        if not re.fullmatch(r"T-\d{10}", id_transaksi):
            raise forms.ValidationError("Format id transaksi harus T-XXXXXXXXXX (T diikuti 10 digit angka).")

        return id_transaksi

    def clean_rating_ulasan(self):
        rating_ulasan = str(self.cleaned_data.get("rating_ulasan"))
        print(rating_ulasan)

        # Ensure it's in the correct decimal format
        if not re.fullmatch(r"[0-4]\.\d{2}|[0-5]\.\d{1}", rating_ulasan):
            raise forms.ValidationError(
                "Format rating ulasan harus dalam bentuk X.XX dengan aturan:\n"
                "- Jika diawali 0-4, harus ada dua angka di belakang koma (contoh: 2.75, 3.99).\n"
                "- Jika angka bulat, contohnya 5 boleh 5.0, 5, atau 5.00"
            )

        return rating_ulasan

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password harus memiliki minimal 8 karakter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password harus mengandung setidaknya satu angka.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password harus mengandung setidaknya satu huruf.")
        if not any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\" for char in password):
            raise forms.ValidationError("Password harus mengandung setidaknya satu karakter spesial.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password dan konfirmasi password harus sama.")

        return cleaned_data

