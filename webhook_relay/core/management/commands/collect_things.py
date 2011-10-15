import os
from imp import load_source
from glob import glob
from django.core.management.base import BaseCommand
from core.models import Emitter, Processor, BaseField


class Command(BaseCommand):
    args = ''
    help = 'dumps all found processors and emitters into the DB'

    def handle(self, *args, **options):
        emitter_files = glob(os.path.join('tasks/emitters/*.py'))
        emitter_files = [emitter for emitter in emitter_files
                         if not emitter.endswith('__init__.py')]
        for emitter_filename in emitter_files:
            filename = os.path.basename(emitter_filename)
            if Emitter.objects.filter(task_name=filename[:-3]).exists():
                continue
            emitter_module = load_source(filename, emitter_filename)
            emitter = Emitter.objects.create(task_name=emitter_module.__package__,
                                             name=emitter_module.__package__)
            for field_name in emitter_module.fields:
                field = BaseField.objects.create(name=field_name)
                emitter.fields.add(field)

        processor_files = glob(os.path.join('tasks/processors/*.py'))
        processor_files = [processor for processor in processor_files
                           if not processor.endswith('__init__.py')]
        for processor_filename in processor_files:
            filename = os.path.basename(processor_filename)
            if Processor.objects.filter(task_name=filename[:-3]).exists():
                continue
            processor_module = load_source(filename, processor_filename)
            processor = Processor.objects.create(task_name=processor_module.__package__,
                                                 name=processor_module.__package__)
            for field_name in processor_module.fields:
                field = BaseField.objects.create(name=field_name)
                processor.fields.add(field)
