from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .utlis import generate_otp_code
from .managers import CustomUserManager

class User(AbstractUser):
    choices_gender = (
        ("male", "ذكر"),
        ("female", "أنثى")
    )
    email = models.EmailField(max_length=80, unique=True, verbose_name=_("Email"))
    image = models.ImageField(upload_to='Photos/%y/%m/%d', null=True, blank=True, verbose_name="الصورة")
    username = models.CharField(max_length=45, verbose_name="اسم المستخدم")
    password = models.CharField(max_length=128, verbose_name="كلمة المرور")
    phoneNumber = models.CharField(null=True, blank=True, max_length=45, verbose_name="رقم الهاتف")
    dateBirth = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    location = models.TextField(null=True, blank=True, verbose_name="العنوان")
    gender = models.TextField(null=True, blank=True, choices=choices_gender, verbose_name="الجنس")
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    otp = models.CharField(max_length=6, null=True, blank=True, verbose_name="كود التحقق")

    def save(self, *args, **kwargs):
        code = generate_otp_code()
        self.otp = code
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.username} - {self.email}'

    class Meta:
        verbose_name = 'المستخدم'
        verbose_name_plural = 'المستخدمين'
