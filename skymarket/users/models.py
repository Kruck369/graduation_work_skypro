from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from django.db.models import TextChoices
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserRoles(TextChoices):
    USER = 'user', _('User')
    ADMIN = 'admin', _('Admin')


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    phone = PhoneNumberField()
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=UserRoles.choices, default=UserRoles.USER)
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def has_perm(self):
        return self.is_admin

    def has_module_perms(self):
        return self.is_admin

    objects = UserManager()
