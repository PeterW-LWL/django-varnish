from atexit import register

from django.conf import settings

from .varnish import VarnishManager

manager = VarnishManager(getattr(settings, 'VARNISH_MANAGEMENT_ADDRS', ()),
                         getattr(settings, 'VARNISH_SECRET', None))
register(manager.close)
