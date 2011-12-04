import sys,os
from django.core.management.base import BaseCommand, CommandError
from twisted.scripts.twistd import run

class Command(BaseCommand):
    
    def handle(self, port='8080', *args, **kwargs):
        self.stdout.write("Starting the processing service")
        sys.path.insert(0, os.path.abspath('./apps/serial/'))
        sys.argv = ['','-ny','apps/serial/shell.tac']
        run()
