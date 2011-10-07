from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = ''
    help = 'Gathers all processors and emitters into the DB'
    
    def handle(self, *args, **kwargs):
        pass
