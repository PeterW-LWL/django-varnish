from django.apps import AppConfig


class VanishApp(AppConfig):
    name = 'varnishapp'

    def ready(self):
        from .recivers import connect

        connect()
