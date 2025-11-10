from django.contrib import admin
from .models import Leaderboard

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_value', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['user__username']