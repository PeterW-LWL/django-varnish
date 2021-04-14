from logging import getLogger

from django.conf import settings
from django.db.models.signals import post_save
from django.utils.module_loading import import_string

from .manager import manager

logger = getLogger('varnishapp')


def connect():
    """
    Connect signal recivers.
    """
    for model in getattr(settings, 'VARNISH_WATCHED_MODELS', ()):
        logger.debug("Setting up `post_save` singal handler for %s", model)
        post_save.connect(
            absolute_url_purge_handler,
            sender=import_string(model)
        )


def absolute_url_purge_handler(sender, **kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'get_absolute_url'):
        logger.debug("Purging %s of %s", instance.get_absolute_url(), instance)
        manager.run('purge.url', r'^%s$' % instance.get_absolute_url())
