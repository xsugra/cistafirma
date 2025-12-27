import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


# Model pre Subscription Plan
class SubscriptionPlan(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=100, unique=True)

    max_watched_companies = models.IntegerField(default=0)
    pdf_reports_per_month = models.IntegerField(default=0)

    price_eur = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'users_subscriptionplan'
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

    def __str__(self):
        return self.name


# Model manažéra pre používateľa
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Emailová adresa je povinná')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Model Používateľa
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,  # Ak uzivatel zmaze plan, ucet mu zostane
        null=True,
        blank=True,
        related_name='users',
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Pre pristup do adminu

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Prihlasujeme sa emailom, nie menom
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
