from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class User(AbstractUser):
    nama = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9._-]+$', 'Nama hanya boleh mengandung huruf, angka, ".", "_", dan "-"'),
        ]
    )
    password = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(8),
            RegexValidator(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', 
                           'Password harus mengandung huruf, angka, dan karakter spesial')
        ]
    )
    tanggal_lahir = models.DateField(
        validators=[]
    )
    nomor_hp = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(r'^\+\d{8,15}$', 'Format nomor HP harus dalam format (kode negara - nomor telepon)')
        ]
    )
    email = models.EmailField(unique=True)
    url_blog = models.URLField(max_length=255)
    deskripsi_diri = models.TextField(
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(1000)
        ]
    )
    id_transaksi = models.CharField(
        max_length=13,  # "T-" + 10 digits = 13 characters
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^T-\d{10}$",
                message="ID Transaksi must start with 'T-' followed by 10 digits."
            )
        ]
    )
    rating_ulasan = models.FloatField(
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(5.00)
        ]
    )

    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions")
    def clean(self):
        """ Custom validation for birth date """
        from django.core.exceptions import ValidationError
        min_birth_date = now().date() - timedelta(days=12*365)  
        if self.tanggal_lahir and self.tanggal_lahir > min_birth_date:
            raise ValidationError({'tanggal_lahir': 'Usia harus minimal 12 tahun'})


