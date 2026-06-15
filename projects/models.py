"""Модели приложения проектов"""
from django.db import models
from django.conf import settings

from constants import LENGTH_200
from validators import validate_github_url

STATUS_ACTIVE = 'открыт'
STATUS_CLOSED = 'закрыт'

class Project(models.Model):
    """Модель проекта"""
    STATUS_CHOICES = [
        ('открыт', 'Открыт'),
        ('закрыт', 'Закрыт'),
    ]

    name = models.CharField(max_length=LENGTH_200, verbose_name='Название проекта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    github_url = models.URLField(blank=True, null=True, validators=[validate_github_url],
                                 verbose_name='Ссылка на GitHub')
    status = models.CharField(max_length=max(len(status[0]) for status in STATUS_CHOICES),
                              choices=STATUS_CHOICES, default=STATUS_ACTIVE,
                              verbose_name='Статус')
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participated_projects',
        blank=True,
        verbose_name='Участники'
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
