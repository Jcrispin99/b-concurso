from django.contrib import admin
from .models import Candidate, Vote


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "get_vote_count", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "slug"]
    readonly_fields = ["created_at", "get_vote_count"]

    def get_vote_count(self, obj):
        return obj.vote_count

    get_vote_count.short_description = "Votos"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "candidate", "voted_at"]
    list_filter = ["candidate", "voted_at"]
    search_fields = ["user__username", "user__email", "candidate__name"]
    readonly_fields = ["voted_at"]
    autocomplete_fields = ["user", "candidate"]
