# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.


"""Defines user roles for the Care variant of Lino Noi."""


from lino.core.roles import UserRole, SiteAdmin
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_noi.lib.tickets.roles import Worker, Triager
from lino.modlib.users.choicelists import UserProfiles
from django.utils.translation import ugettext_lazy as _


class CareRecipient(OfficeUser):
    """A **care recipient** can "call for help" by opening a ticket.

    """
    pass


class CareProvider(CareRecipient, Worker):
    """A **care provider** can offer help to other users.

    """
    pass


class Manager(CareProvider, Triager):
    """

    """
    pass


class SiteAdmin(Manager, SiteAdmin, OfficeStaff):
    """Like a developer, plus site admin and staff"""
    pass


EndUser = CareRecipient
Developer = CareProvider


UserProfiles.clear()
add = UserProfiles.add_item
add('000', _("Anonymous"),        UserRole, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("Care recipient"), CareRecipient, 'recipient')
add('400', _("Care provider"), CareProvider, 'provider')
add('490', _("Manager"), Manager, 'manager')
add('900', _("Administrator"),    SiteAdmin, 'admin')
