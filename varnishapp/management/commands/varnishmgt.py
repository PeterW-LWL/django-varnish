from django.core.management.base import BaseCommand
from varnishapp.manager import manager
from pprint import pprint


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('args')

    def handle(self, *args, **options):
        if args:
            pprint(manager.run(*args))
        else:
            print(manager.help())
