from django.conf.urls import patterns

urlpatterns = patterns(
    'varnishapp.views',
    (r'', 'management'),
)
