from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "candidate", "voted_at"]
    list_filter = ["candidate", "voted_at"]
    search_fields = ["user__username", "user__email", "candidate__name"]
    readonly_fields = ["voted_at"]
    list_display_links = ["id", "user"]

    def has_add_permission(self, request):
        """Solo se pueden crear votos desde la API"""
        return False
