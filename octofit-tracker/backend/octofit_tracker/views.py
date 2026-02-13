from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, 
    TeamSerializer, 
    ActivitySerializer, 
    LeaderboardSerializer, 
    WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing User instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        user_id = str(user._id)
        activities = Activity.objects.filter(user_id=user_id)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def teams(self, request, pk=None):
        """Get all teams for a specific user"""
        user = self.get_object()
        user_id = str(user._id)
        teams = Team.objects.filter(member_ids__contains=user_id)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Team instances.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_id not in team.member_ids:
            team.member_ids.append(user_id)
            team.save()
        
        serializer = self.get_serializer(team)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_id in team.member_ids:
            team.member_ids.remove(user_id)
            team.save()
        
        serializer = self.get_serializer(team)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Activity instances.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """
        Optionally filter activities by user_id
        """
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Leaderboard instances.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    def list(self, request, *args, **kwargs):
        """
        Return user rankings in a format suitable for the frontend.
        For now, aggregate all user activities to create a leaderboard.
        """
        from django.db.models import Sum, Count
        
        # Aggregate activities by user to create leaderboard
        # This is a temporary solution until proper leaderboard data is populated
        leaderboard_data = []
        
        # Get all users with their activities
        users = User.objects.all()
        for user in users:
            user_id = str(user._id)
            activities = Activity.objects.filter(user_id=user_id)
            
            total_activities = activities.count()
            total_points = sum(a.points for a in activities if a.points) or 0
            
            if total_activities > 0 or total_points > 0:
                leaderboard_data.append({
                    'id': user_id,
                    'user': str(user._id),
                    'user_name': user.username or user.email or 'Unknown User',
                    'total_points': total_points,
                    'total_activities': total_activities
                })
        
        # Sort by total_points descending
        leaderboard_data.sort(key=lambda x: x['total_points'], reverse=True)
        
        return Response(leaderboard_data)
    
    def get_queryset(self):
        """
        Optionally filter leaderboard by period
        """
        queryset = Leaderboard.objects.all()
        period = self.request.query_params.get('period', None)
        if period is not None:
            queryset = queryset.filter(period=period)
        return queryset


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Workout instances.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        """
        Optionally filter workouts by difficulty_level
        """
        queryset = Workout.objects.all()
        difficulty = self.request.query_params.get('difficulty_level', None)
        if difficulty is not None:
            queryset = queryset.filter(difficulty_level=difficulty)
        return queryset
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended workouts based on fitness level"""
        fitness_level = request.query_params.get('fitness_level', 'beginner')
        workouts = Workout.objects.filter(
            target_fitness_levels__contains=fitness_level
        )
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
