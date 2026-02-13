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
                'name': 'Tony Stark',
                'email': 'ironman@marvel.com',
                'password': 'hashed_password_1',
                'team': 'Team Marvel',
                'created_at': datetime.now()
            },
            {
                'name': 'Steve Rogers',
                'email': 'captainamerica@marvel.com',
                'password': 'hashed_password_2',
                'team': 'Team Marvel',
                'created_at': datetime.now()
            },
            {
                'name': 'Natasha Romanoff',
                'email': 'blackwidow@marvel.com',
                'password': 'hashed_password_3',
                'team': 'Team Marvel',
                'created_at': datetime.now()
            },
            {
                'name': 'Bruce Banner',
                'email': 'hulk@marvel.com',
                'password': 'hashed_password_4',
                'team': 'Team Marvel',
                'created_at': datetime.now()
            },
            {
                'name': 'Thor Odinson',
                'email': 'thor@marvel.com',
                'password': 'hashed_password_5',
                'team': 'Team Marvel',
                'created_at': datetime.now()
            }
        ]
        
        dc_heroes = [
            {
                'name': 'Bruce Wayne',
                'email': 'batman@dc.com',
                'password': 'hashed_password_6',
                'team': 'Team DC',
                'created_at': datetime.now()
            },
            {
                'name': 'Clark Kent',
                'email': 'superman@dc.com',
                'password': 'hashed_password_7',
                'team': 'Team DC',
                'created_at': datetime.now()
            },
            {
                'name': 'Diana Prince',
                'email': 'wonderwoman@dc.com',
                'password': 'hashed_password_8',
                'team': 'Team DC',
                'created_at': datetime.now()
            },
            {
                'name': 'Barry Allen',
                'email': 'flash@dc.com',
                'password': 'hashed_password_9',
                'team': 'Team DC',
                'created_at': datetime.now()
            },
            {
                'name': 'Arthur Curry',
                'email': 'aquaman@dc.com',
                'password': 'hashed_password_10',
                'team': 'Team DC',
                'created_at': datetime.now()
            }
        ]
        
        all_users = marvel_heroes + dc_heroes
        users_result = db.users.insert_many(all_users)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(users_result.inserted_ids)} users'))
        
        # Populate teams
        self.stdout.write('Populating teams...')
        teams = [
            {
                'name': 'Team Marvel',
                'description': 'Avengers assemble!',
                'members': [user['email'] for user in marvel_heroes],
                'created_at': datetime.now()
            },
            {
                'name': 'Team DC',
                'description': 'Justice League unite!',
                'members': [user['email'] for user in dc_heroes],
                'created_at': datetime.now()
            }
        ]
        teams_result = db.teams.insert_many(teams)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(teams_result.inserted_ids)} teams'))
        
        # Populate activities
        self.stdout.write('Populating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing']
        activities = []
        
        for user in all_users:
            # Create 3-7 random activities for each user
            num_activities = random.randint(3, 7)
            for i in range(num_activities):
                activity = {
                    'user_email': user['email'],
                    'user_name': user['name'],
                    'activity_type': random.choice(activity_types),
                    'duration_minutes': random.randint(20, 120),
                    'calories_burned': random.randint(100, 800),
                    'distance_km': round(random.uniform(1.0, 20.0), 2),
                    'date': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'created_at': datetime.now()
                }
                activities.append(activity)
        
        activities_result = db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(activities_result.inserted_ids)} activities'))
        
        # Populate leaderboard
        self.stdout.write('Populating leaderboard...')
        leaderboard = []
        
        for user in all_users:
            # Calculate total stats from activities
            user_activities = [a for a in activities if a['user_email'] == user['email']]
            total_calories = sum(a['calories_burned'] for a in user_activities)
            total_duration = sum(a['duration_minutes'] for a in user_activities)
            total_distance = sum(a['distance_km'] for a in user_activities)
            
            leaderboard.append({
                'user_email': user['email'],
                'user_name': user['name'],
                'team': user['team'],
                'total_calories': total_calories,
                'total_duration_minutes': total_duration,
                'total_distance_km': round(total_distance, 2),
                'activity_count': len(user_activities),
                'rank': 0,  # Will be calculated based on total_calories
                'updated_at': datetime.now()
            })
        
        # Sort by total_calories and assign ranks
        leaderboard.sort(key=lambda x: x['total_calories'], reverse=True)
        for idx, entry in enumerate(leaderboard):
            entry['rank'] = idx + 1
        
        leaderboard_result = db.leaderboard.insert_many(leaderboard)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(leaderboard_result.inserted_ids)} leaderboard entries'))
        
        # Populate workouts
        self.stdout.write('Populating workouts...')
        workouts = [
            {
                'name': 'Superhero Strength Training',
                'description': 'Build strength like Thor with this intense workout',
                'category': 'Strength',
                'difficulty': 'Advanced',
                'duration_minutes': 45,
                'exercises': [
                    {'name': 'Hammer Curls', 'sets': 4, 'reps': 12},
                    {'name': 'Bench Press', 'sets': 4, 'reps': 10},
                    {'name': 'Squats', 'sets': 4, 'reps': 15},
                    {'name': 'Deadlifts', 'sets': 3, 'reps': 8}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Run like The Flash with this high-intensity cardio routine',
                'category': 'Cardio',
                'difficulty': 'Intermediate',
                'duration_minutes': 30,
                'exercises': [
                    {'name': 'Sprint Intervals', 'sets': 5, 'duration': '2 minutes'},
                    {'name': 'Jump Rope', 'sets': 3, 'duration': '3 minutes'},
                    {'name': 'Burpees', 'sets': 3, 'reps': 20}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Widow Warrior Flexibility',
                'description': 'Enhance agility and flexibility like Black Widow',
                'category': 'Flexibility',
                'difficulty': 'Beginner',
                'duration_minutes': 25,
                'exercises': [
                    {'name': 'Yoga Flow', 'sets': 1, 'duration': '10 minutes'},
                    {'name': 'Dynamic Stretching', 'sets': 2, 'duration': '5 minutes'},
                    {'name': 'Pilates Core', 'sets': 3, 'reps': 15}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Iron Man Endurance',
                'description': 'Build endurance for long missions',
                'category': 'Endurance',
                'difficulty': 'Intermediate',
                'duration_minutes': 60,
                'exercises': [
                    {'name': 'Cycling', 'sets': 1, 'duration': '30 minutes'},
                    {'name': 'Rowing Machine', 'sets': 1, 'duration': '20 minutes'},
                    {'name': 'Plank Hold', 'sets': 3, 'duration': '2 minutes'}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Bat-Combat HIIT',
                'description': 'High-intensity training inspired by Batman',
                'category': 'HIIT',
                'difficulty': 'Advanced',
                'duration_minutes': 40,
                'exercises': [
                    {'name': 'Shadow Boxing', 'sets': 4, 'duration': '3 minutes'},
                    {'name': 'Box Jumps', 'sets': 4, 'reps': 15},
                    {'name': 'Mountain Climbers', 'sets': 4, 'reps': 30},
                    {'name': 'Push-ups', 'sets': 4, 'reps': 20}
                ],
                'created_at': datetime.now()
            },
            {
                'name': 'Aquaman Swim Power',
                'description': 'Master the waters with this swimming workout',
                'category': 'Swimming',
                'difficulty': 'Intermediate',
                'duration_minutes': 45,
                'exercises': [
                    {'name': 'Freestyle Laps', 'sets': 10, 'duration': '2 minutes'},
                    {'name': 'Backstroke', 'sets': 5, 'duration': '3 minutes'},
                    {'name': 'Treading Water', 'sets': 3, 'duration': '5 minutes'}
                ],
                'created_at': datetime.now()
            }
        ]
        
        workouts_result = db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(workouts_result.inserted_ids)} workouts'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {len(all_users)}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {len(teams)}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {len(activities)}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {len(leaderboard)}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {len(workouts)}'))
        
        client.close()
