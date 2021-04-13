from django.apps import AppConfig


class VanishAppConfig(AppConfig):
    name = 'varnishapp'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from .signals import absolute_url_purge_handler
