from rest_framework import serializers
from .models import Vote


class VoteSerializer(serializers.Serializer):
    """Serializer para registrar un voto"""

    candidate_slug = serializers.SlugField(
        help_text="Slug del candidato (ej: ana, maria)"
    )
