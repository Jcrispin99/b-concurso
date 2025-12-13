from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.contrib.auth.models import User


class LoginView(APIView):
    """
    Vista de login con formulario HTML en la Browsable API.
    Envía email y password para obtener el token.
    """

    serializer_class = LoginSerializer

    def get(self, request):
        return Response({"message": "Send POST with email and password"})

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate with username (Django's default auth uses username)
        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )


class RegisterView(APIView):
    """
    Vista de registro con formulario HTML en la Browsable API.
    Campos: username, email, password, dni
    """

    from .serializers import RegisterSerializer

    serializer_class = RegisterSerializer

    def get(self, request):
        return Response(
            {"message": "Send POST with username, email, password, and dni"}
        )

    def post(self, request):
        from .serializers import RegisterSerializer
        from .models import Profile

        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Check if user or DNI already exists
        if User.objects.filter(username=data["username"]).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=data["email"]).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if Profile.objects.filter(dni=data["dni"]).exists():
            return Response(
                {"error": "DNI already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )

        # Create profile with DNI
        Profile.objects.create(user=user, dni=data["dni"])

        # Create token
        token = Token.objects.create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "dni": data["dni"],
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(APIView):
    """
    Vista de perfil protegida por token.
    Requiere header: Authorization: Token <tu_token>
    Muestra datos del usuario y su voto (si existe).
    """

    from rest_framework.authentication import TokenAuthentication
    from rest_framework.permissions import IsAuthenticated

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Obtener información del voto si existe
        vote_info = None
        if hasattr(user, "vote"):
            vote_info = {
                "candidate_name": user.vote.candidate.name,
                "candidate_slug": user.vote.candidate.slug,
                "voted_at": user.vote.voted_at,
            }
        
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
                "vote": vote_info,
                "has_voted": vote_info is not None,
            }
        )


class VotingStatusView(APIView):
    """
    Vista pública para ver el estado de la votación.
    """

    def get(self, request):
        from .models import VotingConfig

        config = VotingConfig.get_config()
        return Response(
            {
                "is_active": config.is_active,
                "started_at": config.started_at,
                "ended_at": config.ended_at,
            }
        )


class VotingStartView(APIView):
    """
    Inicia la votación. Solo para administradores.
    """

    from rest_framework.authentication import TokenAuthentication
    from rest_framework.permissions import IsAdminUser

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        from .models import VotingConfig

        config = VotingConfig.get_config()

        if config.is_active:
            return Response(
                {
                    "error": "La votación ya está activa",
                    "started_at": config.started_at,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        config.start_voting()
        return Response(
            {
                "message": "Votación iniciada exitosamente",
                "is_active": config.is_active,
                "started_at": config.started_at,
            },
            status=status.HTTP_200_OK,
        )


class VotingStopView(APIView):
    """
    Detiene la votación. Solo para administradores.
    """

    from rest_framework.authentication import TokenAuthentication
    from rest_framework.permissions import IsAdminUser

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        from .models import VotingConfig

        config = VotingConfig.get_config()

        if not config.is_active:
            return Response(
                {
                    "error": "La votación ya está detenida",
                    "ended_at": config.ended_at,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        config.stop_voting()
        return Response(
            {
                "message": "Votación detenida exitosamente",
                "is_active": config.is_active,
                "ended_at": config.ended_at,
            },
            status=status.HTTP_200_OK,
        )


# =============================================
# Dashboard Views (HTML)
# =============================================
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count


def is_admin(user):
    """Check if user is admin or superuser"""
    return user.is_staff or user.is_superuser


def dashboard_login(request):
    """Vista de login para el dashboard"""
    if request.user.is_authenticated and is_admin(request.user):
        return redirect("dashboard")

    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and is_admin(user):
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Credenciales inválidas o no tienes permisos de administrador"

    return render(request, "server/login.html", {"error": error})


def dashboard_logout(request):
    """Cerrar sesión"""
    logout(request)
    return redirect("dashboard-login")


@login_required(login_url="dashboard-login")
@user_passes_test(is_admin, login_url="dashboard-login")
def dashboard(request):
    """Vista principal del dashboard"""
    from .models import VotingConfig
    from candidates.models import Candidate
    from votes.models import Vote

    config = VotingConfig.get_config()
    total_votes = Vote.objects.count()

    # Obtener candidatas con conteo de votos
    candidates_qs = Candidate.objects.annotate(vote_count=Count("votes")).order_by(
        "-vote_count", "id"
    )

    candidates = []
    for c in candidates_qs:
        percentage = (c.vote_count / total_votes * 100) if total_votes > 0 else 0
        candidates.append(
            {
                "name": c.name,
                "slug": c.slug,
                "votes": c.vote_count,
                "percentage": round(percentage, 1),
            }
        )

    return render(
        request,
        "server/dashboard.html",
        {
            "voting_config": config,
            "total_votes": total_votes,
            "candidates": candidates,
        },
    )


@login_required(login_url="dashboard-login")
@user_passes_test(is_admin, login_url="dashboard-login")
def dashboard_start_voting(request):
    """Iniciar votación desde dashboard"""
    if request.method == "POST":
        from .models import VotingConfig

        config = VotingConfig.get_config()
        if not config.is_active:
            config.start_voting()
            messages.success(request, "¡Votación iniciada exitosamente!")
        else:
            messages.error(request, "La votación ya está activa")
    return redirect("dashboard")


@login_required(login_url="dashboard-login")
@user_passes_test(is_admin, login_url="dashboard-login")
def dashboard_stop_voting(request):
    """Detener votación desde dashboard"""
    if request.method == "POST":
        from .models import VotingConfig

        config = VotingConfig.get_config()
        if config.is_active:
            config.stop_voting()
            messages.success(request, "¡Votación detenida exitosamente!")
        else:
            messages.error(request, "La votación ya está detenida")
    return redirect("dashboard")
