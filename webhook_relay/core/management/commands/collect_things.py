import os
from glob import glob
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    args = ''
    help = 'dumps all found processors and emitters into the DB'

    def handle(self, *args, **options):
        emitter_files = glob(os.path.join(settings.PROJECT_ROOT, 'tasks/emitters/*.py'))
        for emitter in emitter_files:
            filename = emitter(os.path.basename(emitter))
            if Emitter.objects.filter(filename=filename).exists():
                continue
            emitter_module = imp.load(filename, emitter)
            if hasattr(emitter_module, 'name'):
                Emitter.objects.create(name=emitter_module.name, 
            
        processors = os.path.join(settings.PROJECT_ROOT, 'tasks/processors/*.py')
        pass
