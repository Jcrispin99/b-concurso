"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView, 
    VotingStartView, VotingStopView, VotingStatusView,
    dashboard_login, dashboard_logout, dashboard, 
    dashboard_start_voting, dashboard_stop_voting
)
from candidates.views import CandidateListView, ResultsView
from votes.views import VoteView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("profile/", ProfileView.as_view()),
    # Candidates API
    path("api/candidates/", CandidateListView.as_view(), name="candidates-list"),
    path("api/results/", ResultsView.as_view(), name="results"),
    # Votes API
    path("api/vote/", VoteView.as_view(), name="vote"),
    # Voting Control API
    path("api/voting/status/", VotingStatusView.as_view(), name="voting-status"),
    path("api/voting/start/", VotingStartView.as_view(), name="voting-start"),
    path("api/voting/stop/", VotingStopView.as_view(), name="voting-stop"),
    # Dashboard (HTML Views)
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/login/", dashboard_login, name="dashboard-login"),
    path("dashboard/logout/", dashboard_logout, name="dashboard-logout"),
    path("dashboard/start-voting/", dashboard_start_voting, name="dashboard-start-voting"),
    path("dashboard/stop-voting/", dashboard_stop_voting, name="dashboard-stop-voting"),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
