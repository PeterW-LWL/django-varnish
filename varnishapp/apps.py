from django.apps import AppConfig


class VanishApp(AppConfig):
    name = 'varnishapp'

    # noinspection PyUnresolvedReferences
    def ready(self):
        from .signals import absolute_url_purge_handler
