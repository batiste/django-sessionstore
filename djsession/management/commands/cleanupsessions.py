from django.core.management.base import BaseCommand
from djsession.models import Tableversion

class Command(BaseCommand):
    def handle(self, *args, **options):
        print Tableversion.objects.cleanup_old_session_table()