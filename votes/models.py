from django.db import models
from django.contrib.auth.models import User
from candidates.models import Candidate


class Vote(models.Model):
    """Voto de un usuario por un candidato"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="vote", verbose_name="Usuario"
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name="Candidato",
    )
    voted_at = models.DateTimeField("Fecha de votación", auto_now_add=True)

    class Meta:
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def __str__(self):
        return f"{self.user.username} → {self.candidate.name}"
