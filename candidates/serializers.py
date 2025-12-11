from rest_framework import serializers
from .models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    """Serializer para listar candidatos"""

    class Meta:
        model = Candidate
        fields = ["id", "name", "slug"]
        read_only_fields = ["id"]
