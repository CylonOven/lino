# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines classes related to date ranges.

This is a tested document. To test it, run::

  $ python setup.py test -s tests.UtilsTests.test_dates



"""

from __future__ import unicode_literals

import collections
from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR

DatePeriodValue = collections.namedtuple(
    'DatePeriodValue', ('start_date', 'end_date'))
"""
A named tuple with the following fields:

.. attribute:: start_date

    The start date

.. attribute:: end_date

    The end date
"""


def weekdays(start_date, end_date):
    """Return the number of weekdays that fall in the given period. Does
    not care about holidays.

    Usage examples:

    >>> from lino.utils import i2d
    >>> weekdays(i2d(20151201), i2d(20151231))
    23
    >>> weekdays(i2d(20160701), i2d(20160717))
    11
    >>> weekdays(i2d(20160717), i2d(20160717))
    0
    >>> weekdays(i2d(20160718), i2d(20160717))
    0

    """
    return len(list(rrule(
        DAILY, dtstart=start_date, until=end_date,
        byweekday=(MO, TU, WE, TH, FR))))


