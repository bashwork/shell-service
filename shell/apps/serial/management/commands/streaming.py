from django.core.management.base import BaseCommand, CommandError
from shell.apps.serial.runner import start_server

class Command(BaseCommand):
    
    def handle(self, port='8080', *args, **kwargs):
        self.stdout.write("Starting the streaming service")
        start_server(int(port))
