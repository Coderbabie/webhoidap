from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    # username = None
    name = models.CharField(max_length=200, null=True, help_text="Nhập tên của bạn", verbose_name="Tên")
    email = models.EmailField(unique=True, null=True, help_text="Nhập email của bạn", verbose_name="Email")
    bio = models.TextField(null=True, help_text="Giới thiệu ngắn về bản thân", verbose_name="Tiểu sử")
    avatar = models.ImageField(null=True, default="avatar.svg", help_text="Tải lên ảnh đại diện", verbose_name="Ảnh đại diện")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Topic(models.Model):
    name = models.CharField(max_length=200, help_text="Nhập tên chủ đề", verbose_name="Chủ đề")

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Chọn người tạo phòng", verbose_name="Người tạo phòng")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, help_text="Chọn chủ đề cho phòng", verbose_name="Chủ đề")
    name = models.CharField(max_length=200, help_text="Nhập tên phòng", verbose_name="Tên phòng")
    description = models.TextField(null=True, blank=True, help_text="Nhập mô tả phòng", verbose_name="Mô tả")
    participants = models.ManyToManyField(User, related_name='participants', blank=True, help_text="Chọn thành viên tham gia", verbose_name="Thành viên")
    updated = models.DateTimeField(auto_now=True, help_text="Thời gian cập nhật cuối", verbose_name="Cập nhật lúc")
    created = models.DateTimeField(auto_now_add=True, help_text="Thời gian tạo phòng", verbose_name="Tạo lúc")

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Phòng"
        verbose_name_plural = "Các phòng"

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Người gửi", verbose_name="Người dùng")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, help_text="Phòng gửi tin nhắn", verbose_name="Phòng")
    body = models.TextField(help_text="Nội dung tin nhắn", verbose_name="Tin nhắn")
    updated = models.DateTimeField(auto_now=True, help_text="Thời gian cập nhật tin nhắn", verbose_name="Cập nhật lúc")
    created = models.DateTimeField(auto_now_add=True, help_text="Thời gian tạo tin nhắn", verbose_name="Tạo lúc")

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Tin nhắn"
        verbose_name_plural = "Các tin nhắn"

    def __str__(self):
        return self.body[0:50]
