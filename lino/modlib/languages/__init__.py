# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino.modlib.languages` package is a small plugin which
defines a list of languages (the :class:`Language
<lino.modlib.langguages.models.Language>` model).

It is used mostly by :mod:`lino.modlib.cv`, whose
:class:`LanguageKnowledge <lino.modlib.cv.models.LanguageKnowledge>`
and :class:`Schooling <lino.modlib.cv.models.Schooling>` models have a
`language` field which points to this the :class:`Language
<lino.modlib.langguages.models.Language>` model.

Note that this has nothing to do with the list of languages in your
:attr:`languages <lino.core.site_def.Site.languages>` setting.


.. autosummary::
   :toctree:

    models
    fixtures.few_languages
    fixtures.all_languages

"""
from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Boards")

    def setup_config_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('languages.Languages')
