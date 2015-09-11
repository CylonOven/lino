# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino.modlib.tickets`.

"""

from lino.core.roles import SiteUser


class Triager(SiteUser):
    """A user who is responsible for triaging new tickets.

    """


class Worker(SiteUser):
    """A user who is candidate for working on a ticket.

    """
