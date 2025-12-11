from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):
    """Candidato del concurso"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        unique=True, help_text="Identificador único para el frontend"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"
        ordering = ["id"]

    def __str__(self):
        return self.name

    @property
    def vote_count(self):
        """Retorna el número de votos del candidato"""
        return self.votes.count()


class Vote(models.Model):
    """Voto de un usuario por un candidato"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vote")
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="votes"
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def __str__(self):
        return f"{self.user.username} → {self.candidate.name}"
