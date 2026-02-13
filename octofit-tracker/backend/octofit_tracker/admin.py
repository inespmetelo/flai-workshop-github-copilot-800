from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'fitness_level', 'total_points', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'captain_id', 'total_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'user_id', 'duration', 'distance', 'calories', 'points', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user_id', 'activity_type', 'notes']
    ordering = ['-created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['period', 'period_start', 'period_end', 'last_updated']
    list_filter = ['period', 'period_start']
    ordering = ['-period_start']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty_level', 'estimated_duration', 'estimated_calories', 'created_at']
    list_filter = ['difficulty_level', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
