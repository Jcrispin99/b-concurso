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
from .views import RegisterView, LoginView, ProfileView
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
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
