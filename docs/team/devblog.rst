.. _devblog:

=============================
Start your own developer blog
=============================

This section explains what a **developer blog** is, why you need it,
and how you do it.

Documenting what you do
=======================

The daily work of a software developer includes things like modifying
source code, pushing changes to public repositories, writing comments
in forums, surfing around, reading books, discovering new
technologies, contributing to other projects... 

The basic idea of a developer blog is that you **leave a trace** about
what you have been doing, and that this trace is in a **central
place**.

In your developer blog you simply describe what you are doing. Day by
day. Using plain English language. It is your diary.  

You probably know already one example of a developer blog, namely
Luc's developer blog at :ref:`blog`.


A developer blog *does not need* to be cool, popular, easy to follow,
but it **should rather be**:

- *complete* (e.g. not forget to mention any important code
  change you did) and 
- *concise* (use references to point to places where the reader can
  continue if they are interested).
- *understandable* at least for yourself and for other team members. 

Your blog is a diary, but keep in mind that it is **public**. The
usual rules apply: don't disclose any passwords or private data.
Respect other people's privacy.  Don't quote other author's words
without naming them. Always reference your sources of information.

Luc's blogging system
=====================

:ref:`luc` developed his own way of blogging.  We recommend that you
also start your own developer blog using that way.  

It is free, simple and extensible.  It is based on `Sphinx
<http://sphinx-doc.org/>`_ which is the established standard for
Python projects. It answers well to certain requirements which we
perceive as important:

- A developer uses some editor for writing code, and wants to use that
  same editor for writing his blog.

- A developer usually works on more than one software projects at a
  time.

- A developer should not be locked just because there is no internet
  connection available for a few hours.

We don't know whether Luc's system is better than other systems, but
we recommend to use so that we have a coherent system within the team.
You may of course one day discover a better system, but we recommend
that you give at least a serious try to our system.

As a new new team member, once you've got used to this system, this
will be the easiest way for the other members to follow what you are
doing, where you are stumbling, where you need help.

The developer blog is also part or our collaboration workflow: the
:cmd:`fab ci` command knows where your developer blog is and generates
a commit message which points to today's blog entry.

"Blog" versus "Documentation tree"
==================================

Luc's blogging system uses *daily* entries (maximum one blog entry per
day), and is part of some Sphinx documentation tree.

So don't mix up "a blog" with "a documentation tree".  You will
probably maintain only one *developer blog*, but you will maintain
many different *documentation trees*.  Not every documentation tree
contains a blog.

Luc's developer blog happens to be part of the Lino documentation tree
because Luc is currently the main contributor of Lino. One day we
might decide to split Luc's blog out of the Lino repo into a separate
repository.

You probably will soon have other documentation trees than the one
which contains your blog. For example your first Lino application
might have a local project name "hello", and it might have two
documentation trees, one in English (`hello/docs`) and another in
Spanish (`hello/docs_es`). `fab pd` would upload them to
`public_html/hello_docs` and `public_html/hello_docs_es` respectively.
See :attr:`env.docs_rsync_dest <atelier.fablib.env.docs_rsync_dest>`.


.. _dblog:

The `dblog` project template
============================

To help you get started with blogging in your own developer blog,
there is a project template at https://github.com/lsaffre/dblog


How to configure your blog
==========================

You may find inspiration from the Lino website for configuring your
developer blog.

- Interesting files are:
  :srcref:`docs/conf.py`
  :srcref:`docs/.templates/layout.html`
  :srcref:`docs/.templates/links.html`
