# Command to make sure the database is ready before running the app

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    # Class command to wait for the db

    def handle(self, *args, **options):
        pass