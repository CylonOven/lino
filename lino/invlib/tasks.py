# -*- coding: UTF-8 -*-
# Copyright 2013-2016 by Luc Saffre & Hamza Khchine.
# License: BSD, see LICENSE for more details.

from atelier.invlib.tasks import *

from importlib import import_module

def run_in_demo_projects(ctx, admin_cmd, *more, **args):
    """Run the given shell command in each demo project (see
    :attr:`ctx.demo_projects`).

    """
    cov = args.pop('cov', False)
    for mod in ctx.demo_projects:
        # puts("-" * 80)
        # puts("In demo project {0}:".format(mod))
        print("-" * 80)
        print("In demo project {0}:".format(mod))

        m = import_module(mod)
        # 20160710 p = m.SITE.cache_dir or m.SITE.project_dir
        p = m.SITE.project_dir
        with cd(p):
            # m = import_module(mod)
            if cov:
                args = ["coverage"]
                args += ["run -a"]
                args += ["`which django-admin.py`"]
                datacovfile = ctx.root_dir.child('.coverage')
                if not datacovfile.exists():
                    print('No .coverage file in {0}'.format(ctx.project_name))
                os.environ['COVERAGE_FILE'] = datacovfile
            else:
                args = ["django-admin.py"]
            args += [admin_cmd]
            args += more
            args += ["--settings=" + mod]
            cmd = " ".join(args)
            ctx.run(cmd, pty=True)


@task(name='prep')
def initdb_demo(ctx, cov=False):
    """Run `manage.py initdb_demo` on every demo project."""
    if cov:
        # covfile = ctx.root_dir.child('.coveragerc')
        # if not covfile.exists():
        #     print('No .coveragerc file in {0}'.format(ctx.project_name))
        #     return
        # os.environ['COVERAGE_PROCESS_START'] = covfile
        ctx.run('coverage erase', pty=True)
        run_in_demo_projects(ctx, 'initdb_demo', "--noinput", '--traceback', "--noreload", cov=cov)
    else:
        run_in_demo_projects(ctx, 'initdb_demo', "--noinput", '--traceback', cov=cov)


@task(name='cov', pre=[tasks.call(initdb_demo, cov=True)])
def run_tests_coverage(ctx, html=True, html_cov_dir='htmlcov'):
    """Run all tests and create a coverage report.

    If there a directory named :xfile:`htmlcov` in your project's
    `root_dir`, then it will write a html report into this directory
    (overwriting any files without confirmation).

    """
    covfile = ctx.root_dir.child('.coveragerc')
    if not covfile.exists():
        print('No .coveragerc file in {0}'.format(ctx.project_name))
        return
    if ctx.root_dir.child('pytest.ini').exists():
        ctx.run('coverage combine', pty=True)
        print("Running pytest in {1} within coverage...".format(
            ctx.coverage_command, ctx.project_name))
        with cd(ctx.root_dir):
            ctx.run('py.test --cov=lino --cov-append', pty=True)
        html = False
    else:
        os.environ['COVERAGE_PROCESS_START'] = covfile
        ctx.run('coverage erase', pty=True)
        print("Running {0} in {1} within coverage...".format(
            ctx.coverage_command, ctx.project_name))
        ctx.run('coverage run {}'.format(ctx.coverage_command), pty=True)
    ctx.run('coverage combine', pty=True)
    ctx.run('coverage report', pty=True)
    if html:
        print("Writing html report to %s" % html_cov_dir)
        ctx.run('coverage html -d {0} && open {0}/index.html'.format(
            html_cov_dir), pty=True)
        print('html report is ready.')
    ctx.run('coverage erase', pty=True)


