from django.conf import settings
from django.db.models import get_model
from django.db.models.signals import post_save

from .manager import manager


def absolute_url_purge_handler(sender, **kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'get_absolute_url'):
        manager.run('purge.url', r'^%s$' % instance.get_absolute_url())

for model in getattr(settings, 'VARNISH_WATCHED_MODELS', ()):
    post_save.connect(absolute_url_purge_handler, sender=get_model(*model.split('.')))
