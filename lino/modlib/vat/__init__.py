# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for handling value-added tax (VAT).

This module is designed to work both *with* and *without*
:mod:`lino.modlib.ledger` and :mod:`lino.modlib.declarations`
installed.



.. autosummary::
   :toctree:

    models
    utils
    fixtures.euvatrates



"""

from django.utils.translation import ugettext_lazy as _
from lino import ad


class Plugin(ad.Plugin):
    """See :doc:`/dev/plugins`.

    """
    verbose_name = _("VAT")

    needs_plugins = ['lino.modlib.countries']

    vat_quarterly = False
    """
    Set this to True to support quarterly VAT declarations.
    Used by :mod:`ml.declarations`.
    """

    default_vat_regime = 'private'

    default_vat_class = 'normal'
    """The default VAT class. If this is specified as a string, Lino will
    resolve it at startup into an item of :class:`VatClasses
    <lino.modlib.vat.models.VatClasses>`.

    """

    def get_vat_class(self, tt, item):
        """Return the VAT class to be used for given trade type and given
invoice item. Return value must be an item of
:class:`lino.modlib.vat.models.VatClasses`.

        """
        return self.default_vat_class

    def on_site_startup(self, site):
        vat = site.modules.vat
        if isinstance(self.default_vat_regime, basestring):
            self.default_vat_regime = vat.VatRegimes.get_by_name(
                self.default_vat_regime)
        if isinstance(self.default_vat_class, basestring):
            self.default_vat_class = vat.VatClasses.get_by_name(
                self.default_vat_class)

    def setup_config_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('vat.PaymentTerms')
        m.add_action('vat.VatRates')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('vat.VatRegimes')
        m.add_action('vat.TradeTypes')
        m.add_action('vat.VatClasses')

