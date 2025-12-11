from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.db.models import Count
from .models import Candidate
from .serializers import CandidateSerializer


class CandidateListView(APIView):
    """
    API para listar todos los candidatos del concurso.
    No requiere autenticación (público).
    """

    @extend_schema(
        summary="Listar candidatos",
        description="Obtiene la lista de todos los candidatos del concurso",
        responses={
            200: OpenApiResponse(
                response=CandidateSerializer(many=True),
                description="Lista de candidatos",
            )
        },
        tags=["Candidatos"],
    )
    def get(self, request):
        candidates = Candidate.objects.all().order_by("id")
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)


class ResultsView(APIView):
    """
    API para ver los resultados de la votación.
    Muestra el conteo de votos y porcentaje de cada candidato.
    No requiere autenticación (público).
    """

    @extend_schema(
        summary="Ver resultados de votación",
        description="Obtiene el conteo de votos y porcentajes de cada candidato",
        responses={200: OpenApiResponse(description="Resultados de la votación")},
        tags=["Resultados"],
    )
    def get(self, request):
        from votes.models import Vote

        # Obtener candidatos con conteo de votos
        candidates = Candidate.objects.annotate(vote_count=Count("votes")).order_by(
            "-vote_count", "id"
        )

        total_votes = Vote.objects.count()

        # Construir resultados
        results = []
        for candidate in candidates:
            percentage = (
                (candidate.vote_count / total_votes * 100) if total_votes > 0 else 0
            )
            results.append(
                {
                    "id": candidate.id,
                    "name": candidate.name,
                    "slug": candidate.slug,
                    "votes": candidate.vote_count,
                    "percentage": round(percentage, 2),
                }
            )

        return Response({"total_votes": total_votes, "results": results})
