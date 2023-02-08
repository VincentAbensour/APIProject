# Command to make sure the database is ready before running the app

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as PG2Error
import time

class Command(BaseCommand):
    # Class command to wait for the db

    def handle(self, *args, **options):
        """Entry point for command"""
        self.stdout.write('Waiting for DB')
        db_up = False
        while db_up == False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(PG2Error, OperationalError):
                self.stdout.write('DB unavailable, wait 1sec')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('DB avalaible'))
