from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source='created_at', read_only=True)
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'fitness_level', 'total_points', 'created_at', 'updated_at',
                  'date_joined', 'team_name']
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at', 'date_joined']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None
    
    def get_team_name(self, obj):
        """Get team name for the user"""
        from .models import Team
        user_id_str = str(obj._id)
        # Find team where user_id is in member_ids
        team = Team.objects.filter(member_ids__contains=user_id_str).first()
        return team.name if team else None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'captain_id', 'member_ids', 
                  'total_points', 'created_at', 'updated_at', 'member_count']
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at', 'member_count']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None
    
    def get_member_count(self, obj):
        """Get the count of team members"""
        if obj.member_ids and isinstance(obj.member_ids, list):
            return len(obj.member_ids)
        return 0


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    calories_burned = serializers.IntegerField(source='calories', allow_null=True)
    date = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 'distance', 
                  'calories', 'calories_burned', 'points', 'notes', 'created_at', 'date']
        read_only_fields = ['id', 'points', 'created_at', 'date']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None
    
    def get_user_name(self, obj):
        """Get username for the activity"""
        from bson import ObjectId
        try:
            # Convert string user_id to ObjectId
            if obj.user_id:
                user_object_id = ObjectId(obj.user_id)
                user = User.objects.get(_id=user_object_id)
                return user.username or user.email or 'Unknown User'
        except (User.DoesNotExist, Exception):
            pass
        return 'Unknown User'


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()
    total_activities = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'period', 'period_start', 'period_end', 
                  'user_rankings', 'team_rankings', 'last_updated',
                  'user_name', 'total_points', 'total_activities']
        read_only_fields = ['id', 'last_updated']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None
    
    def get_user_name(self, obj):
        """Placeholder for user name"""
        return 'User'
    
    def get_total_points(self, obj):
        """Placeholder for total points"""
        return 0
    
    def get_total_activities(self, obj):
        """Placeholder for total activities"""
        return 0


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField(source='title')
    duration = serializers.IntegerField(source='estimated_duration')
    calories_estimate = serializers.IntegerField(source='estimated_calories')
    workout_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'title', 'name', 'description', 'difficulty_level', 
                  'target_fitness_levels', 'exercises', 'estimated_duration', 'duration',
                  'estimated_calories', 'calories_estimate', 'workout_type',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None
    
    def get_workout_type(self, obj):
        """Get workout type from difficulty level or default"""
        return obj.difficulty_level.capitalize() if obj.difficulty_level else 'General'
