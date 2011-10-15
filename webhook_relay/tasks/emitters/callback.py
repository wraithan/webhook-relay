from core.models import Data, HookEmitterAssoc
from celery.decorators import task
from urllib import urlencode
from urllib2 import urlopen
import json


fields = ['url', ]


@task(name=__package__)
def emit(hea_id, data_id):
    data = Data.objects.get(id=data_id)
    hea = HookEmitterAssoc.objects.get(id=hea_id)

    encoded_data = urlencode(json.loads(data.post_body))
    urlopen(str(hea.field('url')), data=encoded_data)
