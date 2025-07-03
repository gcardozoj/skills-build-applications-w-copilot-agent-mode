from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_data
from bson import ObjectId
from pymongo import MongoClient
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        try:
            print("Starting database population...")

            # Print database settings
            print("Database settings:")
            print(f"ENGINE: {settings.DATABASES['default']['ENGINE']}")
            print(f"NAME: {settings.DATABASES['default']['NAME']}")
            print(f"HOST: {settings.DATABASES['default']['HOST']}")
            print(f"PORT: {settings.DATABASES['default']['PORT']}")

            # Debugging: Check if MongoDB connection is active
            try:
                client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
                db = client[settings.DATABASES['default']['NAME']]
                print("Collections:", db.list_collection_names())
                
                # List elements in a collection
                collection_name = 'octofit_tracker_user'  # Replace with your collection name
                documents = db[collection_name].find()

                # Print documents
                for document in documents:
                    print(document)
                
                
                print("MongoDB connection is active.")
            except Exception as e:
                print(f"MongoDB connection error: {e}")
                raise

            print("Proceeding with data population...")

            # Debugging: Verify clearing of existing data
            print("Clearing existing data...")
            User.objects.all().delete()
            Team.objects.all().delete()
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()
            print("Existing data cleared.")

            # Debugging: Verify users creation
            try:
                print("Creating users...")
                users = [User(**data) for data in test_data['users']]
                for user in users:
                    print(f"User: {user.username}, ID: {user._id}")
                User.objects.bulk_create(users)
                print("Users created successfully.")
            except Exception as e:
                print(f"An error occurred during users creation: {e}")
                raise

            # Debugging: Verify teams creation
            try:
                print("Creating teams...")
                teams = []
                for team_data in test_data['teams']:
                    members = User.objects.filter(username__in=team_data.pop('members'))
                    team = Team(**team_data)
                    team.save()
                    team.members.clear()
                    team.members.add(*members)
                    teams.append(team)
                    print(f"Team: {team.name}, Members: {[member.username for member in members]}")
                print("Teams created successfully.")
            except Exception as e:
                print(f"An error occurred during teams creation: {e}")
                raise

            # Debugging: Verify activities creation
            try:
                print("Creating activities...")
                activities = []
                for activity_data in test_data['activities']:
                    user = User.objects.get(username=activity_data.pop('user'))
                    activity = Activity(user=user, **activity_data)
                    activities.append(activity)
                Activity.objects.bulk_create(activities)
                print("Activities created successfully.")
            except Exception as e:
                print(f"An error occurred during activities creation: {e}")
                raise

            # Debugging: Verify leaderboard entries creation
            try:
                print("Creating leaderboard entries...")
                leaderboard_entries = []
                for entry_data in test_data['leaderboard']:
                    user = User.objects.get(username=entry_data.pop('user'))
                    entry = Leaderboard(user=user, **entry_data)
                    leaderboard_entries.append(entry)
                Leaderboard.objects.bulk_create(leaderboard_entries)
                print("Leaderboard entries created successfully.")
            except Exception as e:
                print(f"An error occurred during leaderboard entries creation: {e}")
                raise

            # Debugging: Verify workouts creation
            try:
                print("Creating workouts...")
                workouts = [Workout(**data) for data in test_data['workouts']]
                for workout in workouts:
                    print(f"Workout: {workout.name}, ID: {workout._id}")
                Workout.objects.bulk_create(workouts)
                print("Workouts created successfully.")
            except Exception as e:
                print(f"An error occurred during workouts creation: {e}")
                raise

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))

        except Exception as e:
            print(f"An error occurred: {e}")
            raise

if __name__ == "__main__":
    try:
        Command().handle()
    except Exception as e:
        print(f"Unhandled exception: {e}")