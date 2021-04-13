#!/usr/bin/env python3
from distutils.core import setup

from varnishapp import __version__

setup(
    name="django-varnish",
    version=__version__,
    url='https://github.com/justquick/django-varnish',
    author='Justin Quick',
    author_email='justquick@gmail.com',
    long_description=open('README.rst').read(),
    description='''
    Integration between Django and the Varnish HTTP accelerator using the
    management port using telnet
    ''',
    packages=['varnishapp'],
    install_requires=[
        'django>=2,<3'
    ],
)
