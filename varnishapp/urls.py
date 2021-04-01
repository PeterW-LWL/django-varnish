from django.conf.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^get_stats', views.get_stats, name="get_stats"),
    re_path(r'^management', views.management, name="management"),
]
