import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.utils.module_loading import import_string

from .manager import manager

logger = logging.getLogger('varnishapp')


def connect():
    """
    Connect signal recivers.
    """
    for model in getattr(settings, 'VARNISH_WATCHED_MODELS', ()):
        model_class = import_string(model)
        logger.debug("Setting up `post_save` singal handler for %s", model)
        print(model, model_class)
        post_save.connect(
            absolute_url_purge_handler,
            sender=model_class,
        )


def absolute_url_purge_handler(sender, **kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'get_absolute_url'):
        logger.debug("Purging %s for %s",
                     instance.get_absolute_url(), instance)
        print("Success", instance)
        manager.run('purge.url', r'^%s$' % instance.get_absolute_url())
    else:
        logger.debug("Purging failed for %s", instance)
        print("Failed", instance)
