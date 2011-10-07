from core.models import Data, Emitter
from celery.decorators import task
from urllib import urlencode
from urllib2 import urlopen


name = 'callback'
fields = ['url',]

@task(name=name)
def emit(emitter_id, data_id, step):
    data = Data.objects.get(id=data_id)
    hea = emitter.hookemitterassoc_set.filter(hook__id=data.hook_id, step=step)

    urlopen(hea.field('url'), urlencode(data))
