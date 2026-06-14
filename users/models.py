"""Модель пользователя с расширенными полями и функционалом генерации аватарки."""
import random
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image, ImageDraw, ImageFont

from constants import COLORS, LENGTH_124, LENGTH_256, LENGTH_12, AVATAR_SIZE
from validators import validate_github_url


class UserManager(BaseUserManager):
    """Менеджер для модели User, обеспечивающий создание пользователей и суперпользователей."""
    def create_user(self, email, name, surname, password=None, **extra_fields):
        """Создает и сохраняет пользователя с указанным email, именем, фамилией и паролем."""
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя с указанным email, именем, фамилией и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя с расширенными полями и функционалом генерации аватарки."""
    COLORS = COLORS

    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=LENGTH_124, verbose_name='Имя')
    surname = models.CharField(max_length=LENGTH_124, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default-avatar.jpg',
                               verbose_name='Аватар')
    phone = models.CharField(
        max_length=LENGTH_12,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^\+7\d{10}$',
                                   'Номер должен быть в формате +7XXXXXXXXXX (10 цифр после +7)')],
        verbose_name='Телефон'
    )
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub',
                                 validators=[validate_github_url])
    about = models.TextField(max_length=LENGTH_256, blank=True, null=True, verbose_name='О себе')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='Избранные проекты'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def save(self, *args, **kwargs):
        # Приводим телефон к формату +7XXXXXXXXXX
        color = random.choice(self.COLORS)
        if self.phone:
            if self.phone.startswith('8'):
                self.phone = '+7' + self.phone[1:]

        # Генерируем аватарку если её нет или это дефолтная
        if not self.avatar or not self.avatar.name or self.avatar.name == 'avatars/default-avatar.jpg':
            self.avatar = self.generate_avatar()

        super().save(*args, **kwargs)

    def generate_avatar(self):
        """Генерирует аватарку с первой буквой имени на цветном фоне"""
        size = AVATAR_SIZE
        image = Image.new('RGB', size, self.get_random_color())
        draw = ImageDraw.Draw(image)

        # Буква для отображения
        if self.name and isinstance(self.name, str):
            letter = str(self.name)[0].upper() if str(self.name)[0] else '?'
        else:
            letter = '?'

        font = None
        font_size = size[0] // 2
    
        font_paths = [
            # Windows
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            # Mac
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial.ttf",
        ]
        
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except (OSError, IOError):
                continue
        
        if font is None:
            font = ImageFont.load_default()

        try:
            bbox = draw.textbbox((0, 0), letter, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            text_width, text_height = draw.textsize(letter, font=font)
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2 - 3

        draw.text((x, y), letter, fill='white', font=font)

        # Сохраняем в BytesIO
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        return ContentFile(buffer.read(), name=f'avatar_{str(self.email).replace("@", "_")}.png')

    def get_random_color(self):
        """Выбирает случайный цвет из предопределенного списка."""
        return random.choice(COLORS)
    
    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        return f'{self.name} {self.surname}'

    def __str__(self):
        return self.get_full_name()
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
