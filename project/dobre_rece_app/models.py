from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('email address', blank='False', unique='True')
    username = None
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.first_name

class Category(models.Model):
    name = models.CharField(max_length=244)

class Institution(models.Model):
    TYPE_CHOICES = (
    ('charity', 'Charity'),
    ('ngo', 'Non-governmental organisation'),
    ('local', 'Local')
    )

    name = models.CharField(max_length=244)
    description = models.TextField()
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='charity')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=244)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=150)
    zip_code = models.SlugField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=244)
    user = models.ForeignKey(User, blank=True, null=True, default=True, on_delete=models.CASCADE)

    def validate_zip(self, zip_code):
        part_zip = zip_code.split('-')
        for char in zip_code:
            if char not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'):
                raise ValidationError
        if len(part_zip[0]) != 2:
            raise ValidationError('Wprowadź kod pocztowy w formacie "00-000"')
        elif len(part_zip[1]) != 3:
            raise ValidationError('Wprowadź kod pocztowy w formacie "00-000"')

    def validate_phone(self, phone_number):
        if len(phone_number) != 9:
            raise ValidationError('''Numer telefonu stacjonaronego wraz
            z numerem kierunkowym lub numer telefonu komórkowego''')
