from logging import getLogger
from django.conf import settings
from django.db.models import get_model
from django.db.models.signals import post_save

from .manager import manager

logger = getLogger('varnishapp')


def absolute_url_purge_handler(sender, **kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'get_absolute_url'):
        logger.info("Purging %s of %s", instance.get_absolute_url(), instance)
        manager.run('purge.url', r'^%s$' % instance.get_absolute_url())

for model in getattr(settings, 'VARNISH_WATCHED_MODELS', ()):
    logger.info("Setting up `post_save` singal handler for %s", model)
    post_save.connect(absolute_url_purge_handler, sender=get_model(*model.split('.')))
