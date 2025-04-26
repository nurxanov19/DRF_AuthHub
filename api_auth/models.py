from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, is_active=True, is_staff=False, is_superuser=False, **extra_fields):
        if phone is None:
            return ValueError('Telefon kiritish shart')

        user = self.model(phone=phone, password=password, is_active=True, is_staff=False, is_superuser=False, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)   # using=None
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)       # extra_fields.setdefault --> xavfsizroq
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone=phone, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=150, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']      # createsuperuser qilganda so'raladi, bu qismsiz createsuperuser faqat phone ni oladi

    def __str__(self):
        return self.phone

"""
BaseUserManager --> (Foydalanuvchini yaratish logikasi) modeldagi malumotlar ustida amallar bajarishni boshqaradi, create_user, create_superuser kabi metodlarni 
        qo'shish tahrirlab qayta yozish mumkin. Va u eng asosiy Manager klass hisoblanadi (UserManager undan vorislik oladi va unda metodlar tayyor holda)
        
PermissionMixin --> bu class Groups va Permissions qismiga javob beradi. U userni qaysi Groupga tegishli ekanligi va nima huquqlarga 
        ega ekanligini tekshiradi. Uning has_perm(), has_perms(), has_module_perms() metodlari bor.
"""

class OneTimePasswordModel(models.Model):
    phone = models.CharField(max_length=100)
    key = models.CharField(max_length=200)

    is_expired = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    tried = models.PositiveBigIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tried > 3:
            self.is_expired = True
        super(OneTimePasswordModel, self).save(*args, **kwargs)



