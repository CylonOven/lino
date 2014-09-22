# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

- :func:`models_by_base <djangosite.dbutils.models_by_base>`

"""

from django.conf import settings

from djangosite.dbutils import models_by_base

modules = settings.SITE.modules
login = settings.SITE.login
startup = settings.SITE.startup


def show(*args, **kw):
    return login().show(*args, **kw)


