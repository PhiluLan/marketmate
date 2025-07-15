import secrets
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_fields):
        if not email:
            raise ValueError('Email muss angegeben werden')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role='Agentur', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, role, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [('KMU','KMU'), ('Agentur','Agentur')]

    email               = models.EmailField(unique=True)
    role                = models.CharField(max_length=20, default='user')
    first_name          = models.CharField(max_length=30)
    last_name           = models.CharField(max_length=30)
    website_url         = models.URLField(max_length=200)
    company_name  = models.CharField(max_length=100, blank=True)
    industry      = models.CharField(max_length=50, blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url  = models.URLField(blank=True)
    linkedin_url  = models.URLField(blank=True)
    hey_lenny_summary   = models.TextField(null=True, blank=True)
    email_verify_token  = models.CharField(max_length=64, blank=True, null=True)
    is_active           = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.email_verify_token:
            self.email_verify_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
