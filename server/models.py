from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class VotingConfig(models.Model):
    """
    Configuración global de votación. Solo debe existir un registro (singleton).
    """

    is_active = models.BooleanField("Votación Activa", default=False)
    started_at = models.DateTimeField("Fecha de Inicio", null=True, blank=True)
    ended_at = models.DateTimeField("Fecha de Fin", null=True, blank=True)

    class Meta:
        verbose_name = "Configuración de Votación"
        verbose_name_plural = "Configuración de Votación"

    def __str__(self):
        status = "Activa" if self.is_active else "Inactiva"
        return f"Votación: {status}"

    @classmethod
    def get_config(cls):
        """Obtiene o crea la configuración singleton"""
        config, _ = cls.objects.get_or_create(pk=1)
        return config

    def start_voting(self):
        """Inicia la votación"""
        self.is_active = True
        self.started_at = timezone.now()
        self.ended_at = None
        self.save()

    def stop_voting(self):
        """Detiene la votación"""
        self.is_active = False
        self.ended_at = timezone.now()
        self.save()


class Profile(models.Model):
    """
    Perfil extendido del usuario con campos adicionales como DNI.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dni = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.dni}"
