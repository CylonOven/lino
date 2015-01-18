## Copyright 2013-2014 Luc Saffre
## This file is part of the Lino project.

from lino.projects.std.settings import *

class Site(Site):
    
    demo_fixtures = "std demo demo2"
    languages = 'en'
    
    def get_installed_apps(self):
        
        yield super(Site, self).get_installed_apps()
            
        #~ yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        #~ yield 'lino.modlib.changes'
        
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.notes'
        
        yield 'matrix_tutorial'
        
    def setup_choicelists(self):
        
        from lino.modlib.users.choicelists import UserProfiles
        from django.utils.translation import ugettext_lazy as _
        UserProfiles.reset('* office')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),                  '_ _',
            name='anonymous', readonly=True, authenticated=False)
        add('100', _("User"),                       'U U', name='user')
        add('900', _("Administrator"),              'A A', name='admin')

    def setup_menu(self, profile, main):
        m = main.add_menu("entries", _("Entries"))
        m.add_action(Entries)
        m.add_action(EntryTypes)
        m.add_action(CompaniesWithEntryTypes)


SITE = Site(globals())

