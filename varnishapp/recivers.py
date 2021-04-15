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
        url_accessor = None
        if isinstance(model, tuple):
            model, url_accessor = model
        model_class = import_string(model)
        logger.debug("Setting up `post_save` singal handler for %s", model)
        print(model, model_class, url_accessor)
        if url_accessor is None:
            post_save.connect(
                absolute_url_purge_handler,
                sender=model_class,
            )
        else:
            post_save.connect(
                create_handler(url_accessor),
                sender=model_class,
            )


def create_handler(accessor_method):
    def inner(sender, **kwargs):
        instance = kwargs['instance']
        method = getattr(instance, accessor_method, None)
        if method:
            logger.debug("Calling %s on %s", accessor_method, instance)
            purge_url = method()
            logger.debug("Purging %s for %s", purge_url, instance)
            manager.run('purge.url', r'^%s$' % purge_url)
            print("Success", instance, accessor_method)
        else:
            logger.error("%s has no method %s", instance, accessor_method)
            print("Failed", instance, accessor_method)
    return inner


def absolute_url_purge_handler(sender, **kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'get_absolute_url'):
        logger.debug("Purging %s for %s",
                     instance.get_absolute_url(), instance)
        manager.run('purge.url', r'^%s$' % instance.get_absolute_url())
        print("Success", instance)
    else:
        logger.debug("Purging failed for %s", instance)
        print("Failed", instance)
