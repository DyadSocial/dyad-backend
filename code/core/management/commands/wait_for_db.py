import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


# Wait for database to be available before executing command
class Command(BaseCommand):
    def handle(self, *args, **operations):
        self.stdout.write("Waiting for database..")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationlError:
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!)'))


