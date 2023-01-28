"""
User models.
"""
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    """
    User Manager class.
    """

    def create_user(
        self, username, password=None, role=None, deposit=None, **extra_fields
    ):
        """
        Create and save a user with the given username, email, and password.
        """
        if username is None:
            raise TypeError("Users should have a username")

        email = self.normalize_email(username)
        role = "BUYER" if role is None else role
        deposit = 0 if deposit is None else deposit

        user = self.model(username=email, role=role, deposit=deposit, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, username, password=None, role=None, deposit=None, **extra_fields
    ):
        """
        Create and save a super user with the given username, email, and password.
        """
        if password is None:
            raise TypeError("Password should not be none")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, role, deposit, **extra_fields)


class BaseClass(models.Model):
    """
    Base audit class.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class.
        """

        abstract = True


class RoleChoices(models.TextChoices):
    """
    User role choices.
    """

    SELLER = "SELLER"
    BUYER = "BUYER"


class User(AbstractBaseUser, PermissionsMixin):
    """
    User database model.
    Used for storing user details.
    """

    username = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=250, null=False, blank=False)
    deposit = models.IntegerField(
        default=0,
        null=False,
    )
    role = models.CharField(
        max_length=255,
        default=RoleChoices.BUYER,
        choices=RoleChoices.choices,
        null=False,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["role", "deposit"]

    objects = UserManager()

    def __repr__(self):
        """
        String representation of user object.
        """
        return f"{self.username}: {self.role}"

    class Meta:
        """
        Meta class.
        """

        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
