from django.db import models


class Candidate(models.Model):
    """Candidato del concurso"""

    name = models.CharField("Nombre", max_length=100, unique=True)
    slug = models.SlugField(
        "Slug",
        max_length=20,
        unique=True,
        help_text="Identificador único para el frontend (ej: ana, maria)",
    )
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"
        ordering = ["id"]

    def __str__(self):
        return self.name
