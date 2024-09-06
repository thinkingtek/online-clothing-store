from PIL import Image
from django.db import models
from django.utils import timezone
from cart.imports.choices import STATES
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Email Address', max_length=60, unique=True,
                              help_text='This email address will be valiated', error_messages={'unique': 'Sorry this email cannot be used'})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    # class Meta:
    #     ordering = ['date_joined']
    email_verified = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATES)
    address_line = models.CharField(max_length=200)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100)
    landmark = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    terms_and_conditions = models.BooleanField()

    def __str__(self):
        return self.address_line

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(
        default='profile_pix/profile_img.png', upload_to='profile_pix', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.full_name
