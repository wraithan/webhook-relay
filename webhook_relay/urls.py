from django.contrib import admin
from dselector import Parser


admin.autodiscover()
parser = Parser()
url = parser.url

urlpatterns = parser.patterns(
    # base import level
    '',
    # urls
    url(r'hook/{hook:slug}/{slug:slug}', 'core.views.handler', name='handler'),
    url(r'admin/(.*)!', admin.site.root),
)
