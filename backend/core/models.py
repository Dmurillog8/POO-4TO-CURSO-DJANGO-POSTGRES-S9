from django.conf import settings
from django.db import models


class Note(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="notes", verbose_name="propietario",
    )
    title = models.CharField("título", max_length=200)
    body = models.TextField("contenido", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "nota"
        verbose_name_plural = "notas"

    def __str__(self):
        return self.title