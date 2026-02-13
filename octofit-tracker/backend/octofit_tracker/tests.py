from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import date


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            fitness_level='beginner'
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.fitness_level, 'beginner')
        self.assertEqual(self.user.total_points, 0)
    
    def test_user_str(self):
        """Test the string representation of a user"""
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            captain_id='123',
            member_ids=['123', '456']
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.captain_id, '123')
        self.assertEqual(len(self.team.member_ids), 2)
        self.assertEqual(self.team.total_points, 0)
    
    def test_team_str(self):
        """Test the string representation of a team"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='123',
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            points=50
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, 5.0)
        self.assertEqual(self.activity.calories, 300)
        self.assertEqual(self.activity.points, 50)
    
    def test_activity_str(self):
        """Test the string representation of an activity"""
        self.assertEqual(str(self.activity), 'running - 30 min')


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            period='weekly',
            period_start=date(2024, 1, 1),
            user_rankings=[],
            team_rankings=[]
        )
    
    def test_leaderboard_creation(self):
        """Test that a leaderboard can be created"""
        self.assertEqual(self.leaderboard.period, 'weekly')
        self.assertEqual(self.leaderboard.period_start, date(2024, 1, 1))
        self.assertEqual(len(self.leaderboard.user_rankings), 0)


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            title='Beginner Cardio',
            description='A simple cardio workout',
            difficulty_level='beginner',
            target_fitness_levels=['beginner'],
            exercises=[],
            estimated_duration=20,
            estimated_calories=150
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created"""
        self.assertEqual(self.workout.title, 'Beginner Cardio')
        self.assertEqual(self.workout.difficulty_level, 'beginner')
        self.assertEqual(self.workout.estimated_duration, 20)
    
    def test_workout_str(self):
        """Test the string representation of a workout"""
        self.assertEqual(str(self.workout), 'Beginner Cardio')


class UserAPITest(APITestCase):
    def test_create_user(self):
        """Test creating a user via API"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'fitness_level': 'intermediate'
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')


class TeamAPITest(APITestCase):
    def test_create_team(self):
        """Test creating a team via API"""
        data = {
            'name': 'API Team',
            'description': 'Created via API',
            'captain_id': '123',
            'member_ids': ['123']
        }
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, 'API Team')


class ActivityAPITest(APITestCase):
    def test_create_activity(self):
        """Test creating an activity via API"""
        data = {
            'user_id': '123',
            'activity_type': 'cycling',
            'duration': 45,
            'distance': 10.5,
            'calories': 400
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(Activity.objects.get().activity_type, 'cycling')


class WorkoutAPITest(APITestCase):
    def test_create_workout(self):
        """Test creating a workout via API"""
        data = {
            'title': 'HIIT Session',
            'description': 'High intensity interval training',
            'difficulty_level': 'advanced',
            'target_fitness_levels': ['advanced'],
            'exercises': [],
            'estimated_duration': 30,
            'estimated_calories': 350
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
        self.assertEqual(Workout.objects.get().title, 'HIIT Session')
