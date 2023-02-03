from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

MEASURE_UNIT = (("kg", "Kilogram"), ("l", "Litre"), ("pcs", "Pieces"))


class CommonInfo(models.Model):
    created_by = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_created_related",
    )
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_updated_related",
    )
    last_updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(CommonInfo):
    """Represents product type"""

    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(
        max_length=32, choices=MEASURE_UNIT, default=MEASURE_UNIT[1][0]
    )
    description = HTMLField()
    available = models.BooleanField(default=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["name"]),
        ]


class Water(Product):
    volume = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Warehouse(CommonInfo):
    water = models.ForeignKey(
        "core.Water", on_delete=models.CASCADE, related_name="warehouse"
    )
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(
        max_length=32, choices=MEASURE_UNIT, default=MEASURE_UNIT[2][0]
    )

    def __str__(self):
        return f"{self.water} - {self.quantity} {self.unit}"


class Trade(CommonInfo):
    water = models.ForeignKey(
        "core.Water", on_delete=models.CASCADE, related_name="trade"
    )
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(
        max_length=32, choices=MEASURE_UNIT, default=MEASURE_UNIT[2][0]
    )

    def __str__(self):
        return f"{self.water} - {self.quantity} {self.unit} - {self.price} UZS"


class UserManager(DjangoUserManager):
    def _create_user(self, phone, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError("The given phone must be set")
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\d{12}$",
        message="Phone number must be entered in the format: "
        "'998901234567. Exactly 12 digits allowed.",
    )

    phone = models.CharField(
        _("phone"),
        max_length=12,
        db_index=True,
        unique=True,
        help_text=_("Required. 12 digits."),
        validators=[phone_regex],
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
