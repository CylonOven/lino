# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD, see file LICENSE for more details.

"""This defines the :manage:`linod` management command.

.. management_command:: linod

Starts a long-running process that runs scheduled background tasks.

On a development machine you simply run this in a separate
terminal. On a production server we recommend to run this as a daemon
via Supervisor as described in :ref:`admin.linod`.

Independently of whether it is being run as a daemon or not, this
command requires the `schedule <https://github.com/dbader/schedule>`__
package which you must install manually::

  $ pip install schedule

"""

from __future__ import print_function

import time
try:
    import schedule
except ImportError:
    pass  # ignore it here so that autodoc can work without requiring
          # schedule.

# For the schedule logger we set level to WARNING because
# otherwise it would log a message every 10 seconds when
# running an "often" job. We must do this after Django's
# logger configuration.
# import logging
# logging.getLogger('schedule').setLevel(logging.WARNING)

from django.core.management.base import BaseCommand
# import lino
from lino.api import dd


class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--list', '-l', action='store_true',
            dest='list_jobs', default=False,
            help="Just list the jobs, don't run them.")

    def handle(self, *args, **options):
        # lino.startup()
        # lino.site_startup()
        # # rt.startup()
        # schedule.logger.setLevel(logging.WARNING)
        n = len(schedule.jobs)
        if n == 0:
            dd.logger.info("This site has no scheduled jobs.")
            return
        dd.logger.info("%d scheduled jobs:", n)
        for i, job in enumerate(schedule.jobs, 1):
            dd.logger.info("[%d] %s", i, job)
        if options['list_jobs']:
            return
        while True:
            schedule.run_pending()
            time.sleep(1)

