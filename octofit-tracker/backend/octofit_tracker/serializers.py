from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'fitness_level', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'captain_id', 'member_ids', 
                  'total_points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'distance', 
                  'calories', 'points', 'notes', 'created_at']
        read_only_fields = ['id', 'points', 'created_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'period', 'period_start', 'period_end', 
                  'user_rankings', 'team_rankings', 'last_updated']
        read_only_fields = ['id', 'last_updated']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'title', 'description', 'difficulty_level', 
                  'target_fitness_levels', 'exercises', 'estimated_duration', 
                  'estimated_calories', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None
