from json import dumps
from models import Hook, Data
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404


def handler(request, username, slug):
    hook = get_object_or_404(Hook, owner__user__username=username,
                             active=True, slug=slug)
    if request.method == 'POST':
        data = Data.objects.create(post_body=dumps(request.POST), hook=hook)
        hook.next_action(data=data, step=0)
        return HttpResponse('success')
    return HttpResponseBadRequest(status=400)


def index(request):
    return HttpResponse('hi')
