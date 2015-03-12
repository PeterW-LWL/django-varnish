import json
import subprocess

from django.http import HttpResponseRedirect
from manager import manager
from django.shortcuts import render
from django.conf import settings


def get_stats():
    secret = getattr(settings, 'VARNISH_SECRET', '')
    if secret:
        stats = [x[0] for x in manager.run('stats', secret=secret)]
    else:
        stats = [x[0] for x in manager.run('stats')]
    return zip(getattr(settings, 'VARNISH_MANAGEMENT_ADDRS', ()), stats)


def management(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    if 'command' in request.REQUEST:
        kwargs = dict(request.REQUEST.items())
        manager.run(*str(kwargs.pop('command')).split(), **kwargs)
        return HttpResponseRedirect(request.path)

    stats = subprocess.Popen('/usr/bin/varnishstat -j', shell=True, stdout=subprocess.PIPE)\
        .stdout.read()
    stats = json.loads(stats)

    return render(request, 'varnish/report.html', {'stats': stats})
