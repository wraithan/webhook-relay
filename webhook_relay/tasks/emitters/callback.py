from core.models import Data, Emitter
from celery.decorators import task

name = 'callback'

@task()
def emit(emitter_id, data_id, step):
    emitter = Emitter.objects.get(id=emitter_id)
    data = Data.objects.get(id=data_id)
    hea = emitter.hookemitterassoc_set.filter(hook__id=data.hook_id, step=step)
