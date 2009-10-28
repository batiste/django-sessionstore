from django.core.management.base import BaseCommand
from djsession.models import Tableversion

class Command(BaseCommand):
    def handle(self, *args, **options):
        if Tableversion.objects.one_sessions_table_is_empty():
            print "One of the session table is empty. Operation disabled."
            print "Session table are %s and %s" % \
                Tableversion.objects.get_session_table_name()
            print "Check that your server has been restarted properly."
            return
        # execute the rotation
        tv = Tableversion.objects.rotate_table()
        if Tableversion.objects.is_rotation_necessary(tv):
            print "A new rotation is necessary."
        else:
            print "No new rotation is needed for now."
            return
        print "New table rotation version %d:" % tv.current_version
        print "-------------------------------"
        print "Please restart your server so the rotation is taken in account."