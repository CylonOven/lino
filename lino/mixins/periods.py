# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines classes related to date ranges.

"""

from __future__ import unicode_literals
from builtins import object

import logging
logger = logging.getLogger(__name__)

import datetime

try:
    import pytz
except ImportError:
    pytz = None


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.core.exceptions import ValidationError
from django.utils.timezone import is_aware

from atelier.utils import last_day_of_month

from lino.api import dd
from lino.core.model import Model
from lino.utils.format_date import fdl, fds
from lino.utils.ranges import isrange
from lino.core.utils import ParameterPanel
from lino.utils.quantities import Duration


def rangefmt(r):
    return fds(r[0]) + '...' + fds(r[1])



class CombinedDateTime(dd.Model):
    """Mixin for models which have at least one couple of date and time
    fields which form a kind of editable timestamp field.

    """
    class Meta:
        abstract = True

    def get_timezone(self):
        """May get overridden to return the author's timezone."""
        return settings.TIME_ZONE

    def set_datetime(self, name, value):
        """
        Given a datetime `value`, update the two corresponding fields
        `FOO_date` and `FOO_time` (where FOO is specified in `name` which
        must be either "start" or "end").
        """
        if settings.USE_TZ and is_aware(value):
            tz = pytz.timezone(self.get_timezone())
            # dd.logger.info("20151128 set_datetime(%r, %r)", value, tz)
            value = value.astimezone(tz)
            # value = tz.localize(value)
        setattr(self, name + '_date', value.date())
        t = value.time()
        if not t:
            t = None
        setattr(self, name + '_time', t)

    def get_datetime(self, name, altname=None):
        """
        Return a `datetime` value from the two corresponding
        date and time fields.

        `name` can be 'start' or 'end'.
        """
        d = getattr(self, name + '_date')
        t = getattr(self, name + '_time')
        if not d and altname is not None:
            d = getattr(self, altname + '_date')
            if not t and altname is not None:
                t = getattr(self, altname + '_time')
        if not d:
            return None
        if t:
            dt = datetime.datetime.combine(d, t)
        else:
            dt = datetime.datetime(d.year, d.month, d.day)
        if settings.USE_TZ:
            tz = pytz.timezone(self.get_timezone())
            # dd.logger.info("20151128 get_datetime() %r %r", dt, tz)
            dt = tz.localize(dt)
        return dt


class Started(CombinedDateTime):
    """Mixin for models with two fields :attr:`start_date` and
    :attr:`start_time`

    .. attribute:: start_date
    .. attribute:: start_time

    """
    class Meta:
        abstract = True

    start_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Start date"))  # iCal:DTSTART
    start_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Start time"))  # iCal:DTSTART
    #~ start = dd.FieldSet(_("Start"),'start_date start_time')

    def save(self, *args, **kw):
        """
        Fills default value "today" to start_date
        """
        if not self.start_date:
            self.start_date = settings.SITE.today()
        super(Started, self).save(*args, **kw)

class Ended(CombinedDateTime):
    """Mixin for models with two fields :attr:`end_date` and
    :attr:`end_time`
    Models inheriting from this must also inherit from Started.

    .. attribute:: end_date
    .. attribute:: end_time

    """
    class Meta:
        abstract = True
        
    end_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("End Date"))
    end_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("End Time"))

    def get_duration(self):
        """Return the duration in hours."""
        if not self.start_date:
            return None
        if not self.start_time:
            return None
        if not self.end_time:
            return None

        ed = self.end_date or self.start_date

        st = datetime.datetime.combine(self.start_date, self.start_time)
        et = datetime.datetime.combine(ed, self.end_time)

        if et < st:
            return None  # negative duration not supported
        # print 20151127, repr(et), repr(st)
        return Duration(et - st)

    @dd.virtualfield(dd.QuantityField(_("Duration")))
    def duration(self, ar):
        return self.get_duration()





class DatePeriod(Model):

    """A model mixin for models which represent a period whose start and
    end are date fields.

    Designed for usage with
    :class:`lino.modlib.system.choicelists.PeriodEvents`.

    """

    class Meta(object):
        abstract = True

    empty_period_text = ""

    start_date = models.DateField(_("Start date"), blank=True, null=True)
    end_date = models.DateField(_("End date"), blank=True, null=True)

    def full_clean(self, *args, **kw):
        if not isrange(self.start_date, self.end_date):
            raise ValidationError(_("Date period ends before it started."))
        super(DatePeriod, self).full_clean(*args, **kw)

    def get_period(self):
        return (self.start_date, self.end_date)

    def is_past(self):
        return (self.end_date and self.end_date <= dd.today())

    def is_future(self):
        return (self.start_date and self.start_date > settings.SITE.today())

    def get_period_text(self):
        if self.start_date and self.end_date:
            if self.start_date == self.end_date:
                # s = E.tostring(E.b(fdl(self.start_date)))
                s = fdl(self.start_date)
                return pgettext("date", "on %s") % s
            else:
                kw = dict()
                kw.update(a=fdl(self.start_date))
                kw.update(b=fdl(self.end_date))
                return pgettext("date range", "between %(a)s and %(b)s") % kw
        elif self.start_date:
            s = fdl(self.start_date)
            if self.is_future():
                return pgettext("future date range", "from %s") % s
            else:
                return pgettext("date range", "from %s") % s
        elif self.end_date:
            s = fdl(self.end_date)
            return pgettext("date range", "until %s") % s
        return self.empty_period_text

    get_default_start_date = None
    get_default_end_date = None

    @classmethod
    def get_parameter_fields(cls, **fields):
        fields.update(
            start_date=models.DateField(
                _("Period from"), blank=True, null=True,
                default=cls.get_default_start_date,
                help_text=_("Start date of observed period")))
        fields.update(
            end_date=models.DateField(
                _("until"),
                blank=True, null=True,
                default=cls.get_default_end_date,
                help_text=_("End date of observed period")))
        return super(DatePeriod, cls).get_parameter_fields(**fields)


class ObservedPeriod(ParameterPanel):
    """:class:`lino.core.param_panel.ParameterPanel` with two fields
    `start_date` and `end_date` which default to empty.

    """

    get_default_start_date = None
    get_default_end_date = None

    def __init__(self,
                 verbose_name_start=_("Period from"),
                 verbose_name_end=_("until"), **kw):
        kw.update(
            start_date=models.DateField(
                verbose_name_start, blank=True, null=True,
                default=self.get_default_start_date,
                help_text=_("Start date of observed period")),
            end_date=models.DateField(
                verbose_name_end,
                blank=True, null=True,
                default=self.get_default_end_date,
                help_text=_("End date of observed period")),
        )
        super(ObservedPeriod, self).__init__(**kw)


class Yearly(ObservedPeriod):

    """An :class:`ObservedPeriod` for which `start_date` defaults to Jan
    1st and `end_date` to Dec 31 of the current year.

    """

    def get_default_start_date(self):
        D = datetime.date
        return D(D.today().year, 1, 1)

    def get_default_end_date(self):
        D = datetime.date
        return D(D.today().year, 12, 31)


class Monthly(ObservedPeriod):

    """An :class:`ObservedPeriod` which defaults to the current month.

    """

    def get_default_start_date(self):
        return dd.today().replace(day=1)

    def get_default_end_date(self):
        return last_day_of_month(dd.today())


class Today(ParameterPanel):
    """A :class:`ParameterPanel <lino.core.param_panel.ParameterPanel>`
    with a field `today` which defaults to today.

    """
    def __init__(self, verbose_name=_("Situation on"), **kw):
        kw.update(
            today=models.DateField(
                verbose_name, blank=True, null=True,
                default=dd.today,
                help_text=_("Date of observation")),
        )
        super(Today, self).__init__(**kw)


