from profile import Profile
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("User must have an email address!")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role = User.Admin
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    Admin = 0
    Manager = 1
    Printer = 2
    Stack_holder = 3
    ROLE_CHOICES = (
        (Admin, "Admin"),
        (Manager, "Manager"),
        (Stack_holder, "Stack Holder"),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    otp = models.CharField(max_length=8, blank=True, null=True)
    refresh_token = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()
    def __str__(self) -> str:
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True
    def get_role(self):
        if self.role == self.Designer:
            return "Designer"
        elif self.role == self.Reception:
            return "Reception"
        elif self.role == self.SuperDesigner:
            return "SuperDesigner"
        else:
            return "Admin"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to="user/profile_picture",
        blank=True,
        null=True,
    )
    address = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        if self.user:
            return f"{self.user.email}"
        else:
            return "No user associated"
