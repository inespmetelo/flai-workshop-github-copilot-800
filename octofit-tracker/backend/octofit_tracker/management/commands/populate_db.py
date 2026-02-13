from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})
        
        # Create unique index on email field
        self.stdout.write('Creating unique index on user email field...')
        db.users.create_index([('email', 1)], unique=True)
        
        # Sample data - Superheroes
        self.stdout.write('Populating users...')
        marvel_heroes = [
            {
                'username': 'ironman',
                'email': 'ironman@marvel.com',
                'first_name': 'Tony',
                'last_name': 'Stark',
                'fitness_level': 'advanced',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'captainamerica',
                'email': 'captainamerica@marvel.com',
                'first_name': 'Steve',
                'last_name': 'Rogers',
                'fitness_level': 'advanced',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'blackwidow',
                'email': 'blackwidow@marvel.com',
                'first_name': 'Natasha',
                'last_name': 'Romanoff',
                'fitness_level': 'advanced',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'hulk',
                'email': 'hulk@marvel.com',
                'first_name': 'Bruce',
                'last_name': 'Banner',
                'fitness_level': 'intermediate',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'thor',
                'email': 'thor@marvel.com',
                'first_name': 'Thor',
                'last_name': 'Odinson',
                'fitness_level': 'advanced',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        
        dc_heroes = [
            {
                'username': 'batman',
                'email': 'batman@dc.com',
                'first_name': 'Bruce',
                'last_name': 'Wayne',
                'fitness_level': 'advanced',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'superman',
                'email': 'superman@dc.com',
                'first_name': 'Clark',
                'last_name': 'Kent',
                'fitness_level': 'advanced',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'wonderwoman',
                'email': 'wonderwoman@dc.com',
                'first_name': 'Diana',
                'last_name': 'Prince',
                'fitness_level': 'advanced',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'flash',
                'email': 'flash@dc.com',
                'first_name': 'Barry',
                'last_name': 'Allen',
                'fitness_level': 'intermediate',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'username': 'aquaman',
                'email': 'aquaman@dc.com',
                'first_name': 'Arthur',
                'last_name': 'Curry',
                'fitness_level': 'intermediate',
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        
        all_users = marvel_heroes + dc_heroes
        users_result = db.users.insert_many(all_users)
        user_ids = {user['email']: str(user_id) for user, user_id in zip(all_users, users_result.inserted_ids)}
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users_result.inserted_ids)} users'))
        
        # Populate teams
        self.stdout.write('Populating teams...')
        marvel_team_members = [user_ids[user['email']] for user in marvel_heroes]
        dc_team_members = [user_ids[user['email']] for user in dc_heroes]
        
        teams = [
            {
                'name': 'Team Marvel',
                'description': 'Avengers assemble!',
                'captain_id': marvel_team_members[0],
                'member_ids': marvel_team_members,
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'name': 'Team DC',
                'description': 'Justice League unite!',
                'captain_id': dc_team_members[0],
                'member_ids': dc_team_members,
                'total_points': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        teams_result = db.teams.insert_many(teams)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams_result.inserted_ids)} teams'))
        
        # Populate activities
        self.stdout.write('Populating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing']
        activities = []
        
        for user in all_users:
            user_id = user_ids[user['email']]
            # Create 3-7 random activities for each user
            num_activities = random.randint(3, 7)
            for i in range(num_activities):
                activity = {
                    'user_id': user_id,
                    'activity_type': random.choice(activity_types),
                    'duration': random.randint(20, 120),  # minutes
                    'distance': round(random.uniform(1.0, 20.0), 2),  # km
                    'calories': random.randint(100, 800),
                    'points': random.randint(10, 100),
                    'notes': f"Great {random.choice(activity_types).lower()} session!",
                    'created_at': datetime.now() - timedelta(days=random.randint(0, 30))
                }
                activities.append(activity)
        
        activities_result = db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities_result.inserted_ids)} activities'))
        
        # Populate leaderboard - skip for now as we'll calculate it dynamically
        self.stdout.write('Skipping static leaderboard (will be calculated dynamically)...')
        
        # Populate workouts
        self.stdout.write('Populating workouts...')
        workouts = [
            {
                'title': 'Superhero Strength Training',
                'description': 'Build strength like Thor with this intense workout',
                'difficulty_level': 'advanced',
                'target_fitness_levels': ['intermediate', 'advanced'],
                'exercises': [
                    {'name': 'Hammer Curls', 'sets': 4, 'reps': 12},
                    {'name': 'Bench Press', 'sets': 4, 'reps': 10},
                    {'name': 'Squats', 'sets': 4, 'reps': 15},
                    {'name': 'Deadlifts', 'sets': 3, 'reps': 8}
                ],
                'estimated_duration': 45,
                'estimated_calories': 500,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'title': 'Speed Force Cardio',
                'description': 'Run like The Flash with this high-intensity cardio routine',
                'difficulty_level': 'intermediate',
                'target_fitness_levels': ['beginner', 'intermediate'],
                'exercises': [
                    {'name': 'Sprint Intervals', 'sets': 5, 'duration': '2 minutes'},
                    {'name': 'Jump Rope', 'sets': 3, 'duration': '3 minutes'},
                    {'name': 'Burpees', 'sets': 3, 'reps': 20}
                ],
                'estimated_duration': 30,
                'estimated_calories': 400,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'title': 'Widow Warrior Flexibility',
                'description': 'Enhance agility and flexibility like Black Widow',
                'difficulty_level': 'beginner',
                'target_fitness_levels': ['beginner'],
                'exercises': [
                    {'name': 'Yoga Flow', 'sets': 1, 'duration': '10 minutes'},
                    {'name': 'Dynamic Stretching', 'sets': 2, 'duration': '5 minutes'},
                    {'name': 'Pilates Core', 'sets': 3, 'reps': 15}
                ],
                'estimated_duration': 25,
                'estimated_calories': 150,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'title': 'Iron Man Endurance',
                'description': 'Build endurance for long missions',
                'difficulty_level': 'intermediate',
                'target_fitness_levels': ['intermediate', 'advanced'],
                'exercises': [
                    {'name': 'Cycling', 'sets': 1, 'duration': '30 minutes'},
                    {'name': 'Rowing Machine', 'sets': 1, 'duration': '20 minutes'},
                    {'name': 'Plank Hold', 'sets': 3, 'duration': '2 minutes'}
                ],
                'estimated_duration': 60,
                'estimated_calories': 600,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'title': 'Bat-Combat HIIT',
                'description': 'High-intensity training inspired by Batman',
                'difficulty_level': 'advanced',
                'target_fitness_levels': ['advanced'],
                'exercises': [
                    {'name': 'Shadow Boxing', 'sets': 4, 'duration': '3 minutes'},
                    {'name': 'Box Jumps', 'sets': 4, 'reps': 15},
                    {'name': 'Mountain Climbers', 'sets': 4, 'reps': 30},
                    {'name': 'Push-ups', 'sets': 4, 'reps': 20}
                ],
                'estimated_duration': 40,
                'estimated_calories': 550,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'title': 'Aquaman Swim Power',
                'description': 'Master the waters with this swimming workout',
                'difficulty_level': 'intermediate',
                'target_fitness_levels': ['intermediate', 'advanced'],
                'exercises': [
                    {'name': 'Freestyle Laps', 'sets': 10, 'duration': '2 minutes'},
                    {'name': 'Backstroke', 'sets': 5, 'duration': '3 minutes'},
                    {'name': 'Treading Water', 'sets': 3, 'duration': '5 minutes'}
                ],
                'estimated_duration': 45,
                'estimated_calories': 500,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        
        workouts_result = db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts_result.inserted_ids)} workouts'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {len(all_users)}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {len(teams)}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {len(activities)}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {len(workouts)}'))
        
        client.close()
