import json
import subprocess

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .manager import manager


def management(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    if 'command' in request.GET:
        kwargs = dict(request.GET.items())
        manager.run(*str(kwargs.pop('command')).split(), **kwargs)
        return HttpResponseRedirect(request.path)
    if 'command' in request.POST:
        kwargs = dict(request.POST.items())
        manager.run(*str(kwargs.pop('command')).split(), **kwargs)
        return HttpResponseRedirect(request.path)

    try:
        stats = subprocess.Popen(
            '/usr/bin/varnishstat -j',
            shell=True,
            stdout=subprocess.PIPE
        ).stdout.read()
        stats = json.loads(stats)
    except ValueError:
        stats = dict()

    return render(request, 'varnish/report.html', {'stats': stats.iteritems()})
