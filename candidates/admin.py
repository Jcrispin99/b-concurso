from django.contrib import admin
from .models import Candidate


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "slug"]
    readonly_fields = ["created_at"]
    list_display_links = ["id", "name"]
