from distutils.core import setup

setup(
    name = "django-varnish",
    version = '0.2',
    url = 'https://github.com/justquick/django-varnish',
    author = 'Justin Quick',
    author_email= 'justquick@gmail.com',
    long_description=open('README.rst').read(),
    description = 'Integration between Django and the Varnish HTTP accelerator using the management port using telnet',
    packages = ['varnishapp'],
    install_requires = [
        'django>=2,<3'
    ],
)

