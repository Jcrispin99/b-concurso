from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Perfil extendido del usuario con campos adicionales como DNI.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dni = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.dni}"
