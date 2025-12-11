from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from candidates.models import Candidate
from .models import Vote
from .serializers import VoteSerializer


class VoteView(APIView):
    """
    API para votar por un candidato.
    Requiere autenticación con token.
    Un usuario solo puede votar una vez.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer

    @extend_schema(
        summary="Votar por un candidato",
        description="Registra el voto del usuario autenticado por un candidato. Solo se puede votar una vez.",
        request=VoteSerializer,
        responses={
            201: OpenApiResponse(
                description="Voto registrado exitosamente",
                response={
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "message": {"type": "string"},
                        "vote": {
                            "type": "object",
                            "properties": {
                                "candidate": {"type": "string"},
                                "voted_at": {"type": "string", "format": "date-time"},
                            },
                        },
                    },
                },
            ),
            400: OpenApiResponse(description="Ya votó anteriormente o datos inválidos"),
            404: OpenApiResponse(description="Candidato no encontrado"),
        },
        tags=["Votación"],
    )
    def post(self, request):
        # Verificar si ya votó
        if hasattr(request.user, "vote"):
            return Response(
                {
                    "error": "Ya has votado anteriormente",
                    "previous_vote": {
                        "candidate": request.user.vote.candidate.name,
                        "voted_at": request.user.vote.voted_at,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar datos
        serializer = VoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Obtener candidato por slug
        slug = serializer.validated_data["candidate_slug"]
        try:
            candidate = Candidate.objects.get(slug=slug)
        except Candidate.DoesNotExist:
            return Response(
                {"error": f'Candidato con slug "{slug}" no encontrado'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Registrar voto
        vote = Vote.objects.create(user=request.user, candidate=candidate)

        return Response(
            {
                "success": True,
                "message": "Voto registrado exitosamente",
                "vote": {"candidate": candidate.name, "voted_at": vote.voted_at},
            },
            status=status.HTTP_201_CREATED,
        )
