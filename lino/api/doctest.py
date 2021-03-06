# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""A selection of names to be used in tested documents.
"""

from __future__ import print_function

import six
from builtins import str

import django
django.setup()
from lino.api.shell import *
from django.utils import translation
from django.test import Client
import json
from bs4 import BeautifulSoup

from atelier.rstgen import table
from atelier import rstgen
from atelier.rstgen import attrtable
from atelier.utils import unindent

from lino.utils import AttrDict
from lino.utils import i2d
from lino.utils.xmlgen.html import E
from lino.utils.diag import analyzer
from lino.utils import diag
from lino.core import actors
from lino.core.menus import find_menu_item
from lino.sphinxcontrib.actordoc import menuselection_text

from lino.core.menus import Menu
from lino.core.actions import ShowTable

test_client = Client()
# naming it simply "client" caused conflict with a
# `lino_welfare.pcsw.models.Client`

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])


def get_json_dict(username, uri, an='detail'):
    url = '/api/{0}?fmt=json&an={1}'.format(uri, an)
    res = test_client.get(url, REMOTE_USER=username)
    assert res.status_code == 200
    return json.loads(res.content)


def get_json_soup(username, uri, fieldname, **kwargs):
    """Being authentified as `username`, perform a web request to `uri` of
    the test client.

    """
    d = get_json_dict(username, uri, **kwargs)
    html = d['data'][fieldname]
    return BeautifulSoup(html, 'lxml')


def post_json_dict(username, url, data, **extra):
    """Send a POST with given username, url and data. The client is
    expected to respond with a JSON encoded response. Parse the
    response's content (which is expected to contain a dict), convert
    this dict to an AttrDict before returning it.

    """
    res = test_client.post(url, data, REMOTE_USER=username, **extra)
    if res.status_code != 200:
        raise Exception("{} gave status code {} instead of 200".format(
            url, res.status_code))
    return AttrDict(json.loads(res.content))


def check_json_result(response, expected_keys=None, msg=''):
    """Checks the result of response which is expected to return a
    JSON-encoded dictionary with the expected_keys.

    """
    # print("20150129 response is %r" % response.content)
    if response.status_code != 200:
        raise Exception(
            "Response status ({0}) was {1} instead of 200".format(
                msg, response.status_code))
    try:
        result = json.loads(response.content)
    except ValueError as e:
        raise Exception("{0} in {1}".format(e, response.content))
    if expected_keys is not None:
        if set(result.keys()) != set(expected_keys.split()):
            raise Exception("'{0}' != '{1}'".format(
                ' '.join(list(result.keys())), expected_keys))
    return result


def demo_get(
        username, url_base, json_fields=None,
        expected_rows=None, **kwargs):
    from django.conf import settings
    case = HttpQuery(username, url_base, json_fields,
                     expected_rows, kwargs)
    # Django test client does not like future pseudo-unicode strings
    # See #870
    url = six.text_type(settings.SITE.buildurl(case.url_base, **case.kwargs))
    # print(20160329, url)
    if True:
        msg = 'Using remote authentication, but no user credentials found.'
        try:
            response = self.client.get(url)
            raise Exception("Expected '%s'" % msg)
        except Exception:
            pass
            #~ self.tc.assertEqual(str(e),msg)
            #~ if str(e) != msg:
                    #~ raise Exception("Expected %r but got %r" % (msg,str(e)))

    if False:
        # removed 20161202 because (1) it was relatively useless and
        # (2) caused a PermissionDenied warning
        response = test_client.get(url, REMOTE_USER=six.text_type('foo'))
        if response.status_code != 403:
            raise Exception(
                "Status code %s other than 403 for anonymous on GET %s" % (
                    response.status_code, url))

    response = test_client.get(url, REMOTE_USER=str(case.username))
    # try:
    if True:
        user = settings.SITE.user_model.objects.get(
            username=case.username)
        result = check_json_result(
            response, case.json_fields,
            "GET %s for user %s" % (url, user))

        num = case.expected_rows
        if num is not None:
            if not isinstance(num, tuple):
                num = [num]
            if result['count'] not in num:
                msg = "%s got %s rows instead of %s" % (
                    url, result['count'], num)
                raise Exception(msg)

    # except Exception as e:
    #     print("%s:\n%s" % (url, e))
    #     raise


def screenshot(obj, filename, rstname, username='robin'):
    """Insert a screenshot of the detail window for the given database
    object.

    Usage example in the source code of
    http://xl.lino-framework.org/specs/holidays.html.

    Problems: doesn't seem to wait long enough and
    therefore produces a white .png file.

    How to specify the filename? the current directory when doctest is
    running is normally the project root, but that's not sure. Best
    place would be the same directory as the rst file, but how to know
    that name from within a tested snippet?

    """
    from lino.api.selenium import Album, runserver

    assert filename.endswith('.png')
    assert rstname.endswith('.rst')

    self = dd.plugins.extjs.renderer
    ba = obj.get_detail_action()
    uri = self.get_detail_url(ba.actor, obj.pk)
    print(uri)

    def f(driver):
        app = Album(driver)
        driver.get("http://127.0.0.1:8000" + uri)
        # driver.get(uri)
        app.stabilize()
        if not driver.get_screenshot_as_file(filename):
            app.error("Failed to create {0}".format(filename))

    runserver(settings.SETTINGS_MODULE, f)
        

def show_menu_path(spec, language=None):

    def doit():
        # profile = ar.get_user().profile
        # menu = settings.SITE.get_site_menu(settings.SITE.kernel, profile)
        # mi = menu.find_item(spec)
        mi = find_menu_item(spec)
        if mi is None:
            raise Exception("Invalid spec {0}".format(spec))
        print(menuselection_text(mi))

    if language:
        with translation.override(language):
            return doit()
    return doit()

    # items = [mi]
    # p = mi.parent
    # while p:
    #     items.insert(0, p)
    #     p = p.parent
    # return " --> ".join([i.label for i in items])


def noblanklines(s):
    """Remove blank lines from output. This is used to increase
    readability when some expected output would otherweise contain
    disturbing `<BLANKLINE>` which are not relevant to the test
    itself.

    """
    return '\n'.join([ln for ln in s.splitlines() if ln.strip()])


def show_choices(username, url):
    """Print the choices returned via web client."""
    response = test_client.get(url, REMOTE_USER=username)
    if response.status_code != 200:
        raise Exception(
            "Response status ({0}) was {1} instead of 200".format(
                url, response.status_code))

    result = json.loads(response.content)
    for r in result['rows']:
        print(r['text'])
        # print(r['value'], r['text'])

from django.db.models import Model
from lino.core.actions import Action
from lino.core.tables import AbstractTable
from lino.core.boundaction import BoundAction


def show_fields(model, fieldnames=None):
    """Print an overview description of the specified fields of the
    specified model.

    """
    cells = []
    cols = ["Internal name", "Verbose name", "Help text"]
    if isinstance(model, BoundAction):
        get_field = model.action.parameters.get
        if fieldnames is None:
            fieldnames = model.action.params_layout
    elif isinstance(model, Action):
        get_field = model.parameters.get
        if fieldnames is None:
            fieldnames = model.params_layout.main
    elif issubclass(model, Model):
        get_field = model._meta.get_field
        if fieldnames is None:
            fieldnames = [f.name for f in model._meta.get_fields()]
    elif issubclass(model, AbstractTable):
        get_field = model.parameters.get
        if fieldnames is None:
            fieldnames = model.params_layout.main
    if isinstance(fieldnames, six.string_types):
        fieldnames = fieldnames.split()
    for n in fieldnames:
        fld = get_field(n)
        if fld is not None and hasattr(fld, 'verbose_name'):
            cells.append([n,
                          fld.verbose_name,
                          unindent(fld.help_text or '')])

    print(table(cols, cells).strip())


def py2rst(x):
    return diag.py2rst(x, True)


def show_dialog_actions():
    return analyzer.show_dialog_actions(True)


def walk_menu_items(username=None, severe=False):
    """Walk through all menu items which run a :class:`ShowTable
    <lino.core.actions.ShowTable>` action, showing how many data rows
    the grid contains.

    """
    def doit(user_type):
        mnu = settings.SITE.get_site_menu(None, user_type)
        items = []
        for mi in mnu.walk_items():
          if mi.bound_action:
            if isinstance(mi.bound_action.action, ShowTable):
                mt = mi.bound_action.actor
                url = 'api/{}/{}'.format(mt.app_label, mt.__name__)
                url = six.text_type(settings.SITE.buildurl(url, fmt='json'))

                item = menuselection_text(mi) + " : "
                try:
                    response = test_client.get(url, REMOTE_USER=six.text_type(username))
                    result = check_json_result(
                        response, None,
                        "GET %s for user %s" % (url, username))
                    item += str(result['count'])
                except Exception as e:
                    if severe:
                        raise
                    else:
                        item += str(e)
                items.append(item)

        s = rstgen.ul(items)
        print(s)

    if settings.SITE.user_types_module:
        ar = settings.SITE.login(username)
        with translation.override(ar.user.language):
            doit(ar.user.profile)
    else:
        doit(None)
        
        
