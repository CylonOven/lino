# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.accounts`.

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings

from lino.api import dd
from lino import mixins
from django.utils.translation import ugettext_lazy as _

from .choicelists import AccountTypes


class Chart(mixins.BabelNamed):
    "A collection of accounts."
    class Meta:
        verbose_name = _("Account Chart")
        verbose_name_plural = _("Account Charts")

    def get_account_by_ref(self, ref):
        try:
            #~ print 20121203, dict(ref=account,chart=self.journal.chart)
            return Account.objects.get(ref=ref, chart=self)
        except Account.DoesNotExist:
            raise Warning("No Account with reference %r" % ref)


class Charts(dd.Table):
    model = Chart
    required = dd.required(user_level='manager')

    insert_layout = """
    name
    """

    detail_layout = """
    id name
    GroupsByChart
    """


#~ class Group(mixins.BabelNamed,mixins.Sequenced):


class Group(mixins.BabelNamed):
    "A group of accounts."
    class Meta:
        verbose_name = _("Account Group")
        verbose_name_plural = _("Account Groups")
        unique_together = ['chart', 'ref']

    chart = models.ForeignKey(Chart)
    ref = dd.NullCharField(
        max_length=settings.SITE.plugins.accounts.ref_length)
    #~ ref = models.CharField(max_length=100)
    account_type = AccountTypes.field(blank=True)
    # help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)


class Groups(dd.Table):
    
    model = 'accounts.Group'
    required = dd.required(user_level='manager')
    order_by = ['chart', 'ref']
    column_names = 'chart ref name account_type *'
    #~ required = dict(user_groups=['debts'],user_level='manager')
    #~ required_user_groups = ['debts']
    #~ required_user_level = UserLevels.manager

    insert_layout = """
    name
    account_type ref
    """

    detail_layout = """
    ref name
    account_type id
    #help_text
    AccountsByGroup
    """


class GroupsByChart(Groups):
    master_key = 'chart'
    order_by = ['ref']
    column_names = 'ref name account_type *'


class Account(mixins.BabelNamed, mixins.Sequenced):

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        unique_together = ['chart', 'ref']
        ordering = ['ref']

    chart = models.ForeignKey(Chart)
    group = models.ForeignKey(Group)
    #~ ref = models.CharField(max_length=100)
    ref = dd.NullCharField(
        max_length=settings.SITE.plugins.accounts.ref_length)
    #~ chart = models.ForeignKey(Chart)
    type = AccountTypes.field()  # blank=True)
    # help_text = dd.RichTextField(_("Introduction"),format="html",blank=True)

    def full_clean(self, *args, **kw):
        if self.group_id is not None:
            self.chart = self.group.chart
            if not self.ref:
                self.ref = str(self.chart.account_set.count() + 1)
            if not self.name:
                self.name = self.group.name
            #~ if not self.type:
            self.type = self.group.account_type
            #~ if not self.chart:
                #~ self.chart = self.group.chart
        super(Account, self).full_clean(*args, **kw)

    def __unicode__(self):
        return "(%(ref)s) %(title)s" % dict(
            ref=self.ref,
            title=settings.SITE.babelattr(self, 'name'))


class Accounts(dd.Table):
    model = Account
    required = dd.required(user_level='manager')
    order_by = ['ref']
    column_names = "ref name group *"
    insert_layout = """
    ref group type
    name
    """
    detail_layout = """
    ref name
    group type
    # help_text
    """


class AccountsByGroup(Accounts):
    required = dd.required()
    master_key = 'group'
    column_names = "ref name *"


dd.add_user_group('accounts', dd.plugins.accounts.verbose_name)

