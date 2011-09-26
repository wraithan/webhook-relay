from json import dumps
from models import Hook, Data
from django.shortcuts import get_object_or_404


def handler(request, username, slug):
    if request.method == 'POST':
        hook = get_object_or_404(Hooks, owner__user__username=username, active=True, slug=slug)
        data = Data.objects.create(post_body=dumps(request.POST), hook=hook)
        hook.next_action(data=data, step=0)
    return
