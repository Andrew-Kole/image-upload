"""
The custom command that helps to avoid situation,
when db is not ready and app tries to make requests to it.
In this case app will crush,
so this command make sure that db is available for interactions.
"""

from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """represents the custom command that 'freezes' app
    until the database will be available"""

    def handle(self, *args, **options):
        """Entry point for the command"""
        self.stdout.write('Waiting for db...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Wait a bit more...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Thanks for patience, '
                                             'now you can use db.'))
