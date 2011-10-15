from django.conf.urls.defaults import include
from django.contrib import admin
from dselector import Parser


admin.autodiscover()
parser = Parser()
url = parser.url

urlpatterns = parser.patterns(
    # base import level
    '',
    # urls
    url(r'', 'core.views.index', name='index'),
    url(r'v1/{username:slug}/{slug:slug}',
        'core.views.handler',
        name='handler'),
    url(r'admin/(.*)!', include(admin.site.urls)),
)
