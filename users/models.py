from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'user', _('Обычный пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    email = models.EmailField(_('email address'), unique=True)
    bio = models.CharField(max_length=250, blank=True)
    role = models.CharField(
        max_length=9, choices=UserRole.choices, default=UserRole.USER
    )
    confirmation_code = models.CharField(max_length=15)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    STAFF = [UserRole.MODERATOR, UserRole.ADMIN]

    @property
    def is_admin_or_moder(self):
        return self.role in self.STAFF or self.is_superuser

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN or self.is_superuser
