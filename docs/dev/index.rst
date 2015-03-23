=================
Developer's Guide
=================

This is the central meeting place for Lino application developers.  We
are doing our best to grow this into a pedagogically meaningful
sequence of articles.

Getting started
===============


.. toctree::
   :maxdepth: 1
   :hidden:

   install
   /tutorials/hello/index
   /tutorials/polls/mysite/index
   /tutorials/dumpy
   /tutorials/tables/index
   /tutorials/lets/index

- :doc:`/dev/install` : How to install Lino. System requirements. "Released
  version" versus "Development version". How to run Lino's test
  suite.

- :doc:`/tutorials/hello/index` : The first Lino application running
  on your machine. It's easier than with Django. A ``settings.py`` and
  a ``manage.py``. Initialize a demo database. Run a development
  server.

- :doc:`/tutorials/polls/mysite/index` : We convert the “Polls”
  application from Django’s tutorial into a Lino application. This
  will introduce some differences between Lino and Django.

- :doc:`/tutorials/dumpy` : The ``initdb`` and ``initdb_demo``
  commands.  Playing with fixtures.  Writing your own fixture.

- :doc:`/tutorials/tables/index` : Models, tables and views. What is a
  table? Designing your tables. Using tables without a web server.

- :doc:`/tutorials/lets/index` : What is a technical specification?
  Describing a database structure. Designing your tables. Writing demo
  data. Writing test cases. Menu structure and main page. Form layouts.


Getting acquaintained
=====================

- :doc:`settings` : The Django settings module. How Lino integrates
  into Django settings. Inheriting settings.
- :doc:`application` : An app is not an application.
- :doc:`plugins` : Why we need plugins. Configuring plugins.
- :doc:`users` : Why do we replace Django's user management. Passwords.
- :doc:`site` : Instantiating a `Site`.  Specifying the
  `INSTALLED_APPS`. Additional local apps.
- :doc:`dump2py` : Python dumps
- :doc:`site_config` : The SiteConfig used to store "global" site-wide
  parameters in the database.
- :doc:`languages` : if you write applications for users who don't
  speak English.
- :doc:`i18n` : About "internationalization" and "translatable strings".
- :doc:`menu` : Standard items of a main menu
- :doc:`actors` :
- :doc:`choicelists` :
- :doc:`parameters` :

- :doc:`ar` : Using action requests
- :doc:`html` : Generating HTML
- :doc:`custom_actions` : Writing custom actions
- :doc:`gfks` : Lino and `GenericForeignKey` fields

- :doc:`/tutorials/letsmti/index` :
- :doc:`/tutorials/layouts` :
- :doc:`/tutorials/vtables/index` :
- :doc:`actions` :
- :doc:`/tutorials/actions/index` :
- :doc:`/tutorials/mldbc/index` :
- :doc:`/tutorials/human/index` :
- :doc:`apps` : Plugin inheritance
- :doc:`printing` : (TODO)
- :doc:`accounting` : Accounting explained to Python developers.

.. toctree::
   :maxdepth: 1
   :hidden:

   settings
   application
   plugins
   site
   dump2py
   site_config
   users
   languages
   i18n
   menu
   actors
   choicelists
   parameters
   ar
   html
   custom_actions
   gfks
   /tutorials/letsmti/index
   /tutorials/layouts
   /tutorials/vtables/index
   actions
   /tutorials/actions/index
   /tutorials/mldbc/index
   /tutorials/human/index
   apps
   printing
   accounting
   

Reference
=========

.. toctree::
   :maxdepth: 1

   layouts

   ml/index
   

Special topics
==============

.. toctree::
   :maxdepth: 1

   /tutorials/addrloc/index
   /tutorials/mti/index
   /tutorials/sendchanges/index
   /tutorials/actors/index
   /tutorials/de_BE/index
   /tutorials/watch_tutorial/index
   /tutorials/workflows_tutorial/index
   /tutorials/matrix_tutorial/index

   /tutorials/auto_create/index
   /tutorials/pisa/index
   /tutorials/input_mask/index
   /tutorials/gfks/index

Drafts
======
   
.. toctree::
   :maxdepth: 1

   /tutorials/tested_docs/index
   startup
   perms
   workflows
   pull
   translate/index

   testing
   
   help_texts
   userdocs
   signals
   intro
   style
   datamig
   versioning


Other
-----

.. toctree::
   :maxdepth: 1

   /changes
   /todo
   /tested/index
   git
   /ref/index



.. toctree::
   :hidden:

   tables
   fields
   ad
   dd
   rt
   mixins
   /tutorials/index
