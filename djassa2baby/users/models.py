import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from core.models.role import Role


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class ConcatOp(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"

class User(AbstractUser):
    # class Meta:
    #     db_table = 'custom_user'

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.GeneratedField(
        expression=ConcatOp('first_name', models.Value(''),'last_name'),
        output_field=models.CharField(max_length=100), db_persist=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    delivery_adresse = models.CharField(max_length=50,null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.full_name
