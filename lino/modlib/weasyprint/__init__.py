# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""This plugins installs two build methods for generating
:doc:`printable documents </admin/printing>` using `weasyprint
<http://weasyprint.org/>`__.

Applications which use this plugin must also add `'weasyprint'` to
their :ref:`install_requires`.  They should also add `'cairocffi<0.7'`
(see :ticket:`1119`). Or install it using pip::

  $ pip install 'cairocffi<0.7' weasyprint

The build methods defined by this plugin have the same input template,
whose ending must be :xfile:`.weasy.html`.  Both methods then render
the input template through Jinja with the standard context variables
(defined by :meth:`get_printable_context
<lino.core.model.Model.get_printable_context>`.  The base build method
:class:`WeasyBuildMethod
<lino.modlib.weasyprint.choicelists.WeasyBuildMethod>` then returns
this HTML output "as is", the other method runs `weasyprint
<http://weasyprint.readthedocs.io>`__ over the HTML file to convert it
to a :file:`.pdf` file.


.. autosummary::
   :toctree:

    choicelists
    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("WeasyPrint")

    # def on_ui_init(self, kernel):
    #     """
    #     This is being called from
    #     :meth:`lino.core.kernel.Kernel.kernel_startup`.

    #     Lino has an automatic and currently not configurable method
    #     for building Jinja's template loader. It looks for
    #     a "config" subfolder in the following places:

    #     - the project directory :attr:`lino.core.site.Site.project_dir`
    #     - the directories of each installed app

    #     """
    #     from .renderer import WeasyRenderer
    #     self.renderer = WeasyRenderer(self)
