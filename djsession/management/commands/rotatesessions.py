from django.core.management.base import BaseCommand
from djsession.models import Tableversion

class Command(BaseCommand):
    def handle(self, *args, **options):
        tv = Tableversion.objects.rotate_table()
        print "Current rotation version %d:" % tv.current_version
        print "It happened %s" % tv.latest_rotation
        if Tableversion.objects.one_sessions_table_is_empty():
            print "One of the session table is empty"
        if Tableversion.objects.is_rotation_necessary(tv):
            print "A new rotation is necessary"
        else:
            print "No new rotation is needed"