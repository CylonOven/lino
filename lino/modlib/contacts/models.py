# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.contacts`.

- The :class:`Partner` model (and its two subclasses
  :class:`Person` and :class:`Company`)

- A :class:`CompanyType` model can be used to classify companies.

- The :class:`Role` and :class:`RoleType` models store "who is who"
  information.

  TODO: rename :class:`Role` to "Contact", :class:`RoleType` to "Role"
  and field `Contact.type` to `role`.  Move Partner, Person and
  Company into a separate plugin "partners".

.. autosummary::

"""


from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

from lino.utils import join_words
from lino.utils import join_elems

from lino.modlib.countries.mixins import AddressLocation

from lino.utils import mti
from lino.utils.xmlgen.html import E
from lino.utils.addressable import Addressable


from .mixins import ContactRelated, PartnerDocument, OldCompanyContact

from .utils import name2kw


PARTNER_NUMBERS_START_AT = 100  # used for generating demo data and tests


class Partner(mixins.Polymorphic, AddressLocation, Addressable):
    """
    A Partner is any physical or moral person for which you want to
    keep contact data (address, phone numbers, ...).

    A :class:`Partner` can act as the recipient of a sales invoice, as
    the sender of an incoming purchases invoice, ...

    A Partner has at least a name and usually also an "official" address.

    Predefined subclasses of Partners are :class:`Person` for physical
    persons and :class:`Company` for companies, organisations and any
    kind of non-formal Partners.

    .. attribute:: name

    The full name of this partner. Used for alphabetic
    sorting. Subclasses may fill this field automatically, e.g. saving
    a :class:`Person` will automatically set her `name` field to
    "last_name, first_name".

    .. attribute:: email

    The primary email address.


    """
    preferred_foreignkey_width = 20
    # preferred width for ForeignKey fields to a Partner

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Partner')
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    name = models.CharField(max_length=200, verbose_name=_('Name'))

    language = dd.LanguageField()

    email = models.EmailField(_('E-Mail'), blank=True)  # ,null=True)
    url = models.URLField(_('URL'), blank=True)
    phone = models.CharField(_('Phone'), max_length=200, blank=True)
    gsm = models.CharField(_('GSM'), max_length=200, blank=True)
    fax = models.CharField(_('Fax'), max_length=200, blank=True)

    remarks = models.TextField(_("Remarks"), blank=True)  # ,null=True)

    is_person = mti.EnableChild(
        "contacts.Person",
        verbose_name=_("is Person"),
        help_text=_("Whether this Partner is a Person."))

    is_company = mti.EnableChild(
        "contacts.Company",
        verbose_name=_("is Company"),
        help_text=_("Whether this Partner is a Company."))

    print_labels = dd.PrintLabelsAction()

    def on_create(self, ar):
        self.language = ar.get_user().language
        if not self.country:
            sc = settings.SITE.site_config
            if sc.site_company:
                self.country = sc.site_company.country
        super(Partner, self).on_create(ar)

    def save(self, *args, **kw):
        if self.id is None:
            sc = settings.SITE.site_config
            if sc.next_partner_id is not None:
                self.id = sc.next_partner_id
                sc.next_partner_id += 1
                sc.save()
        #~ logger.info("20120327 Partner.save(%s,%s)",args,kw)
        super(Partner, self).save(*args, **kw)

    def __unicode__(self):
        #~ return self.name
        return self.get_full_name()

    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()

    def get_full_name(self, *args, **kw):
        """\
Returns a one-line string representing this Partner.
The default returns simply the `name` field, ignoring any parameters,
but e.g. :class:`Human` overrides this.
        """
        return self.name
    full_name = property(get_full_name)

    @dd.displayfield(_("Name"))
    def name_column(self, request):
        #~ return join_words(self.last_name.upper(),self.first_name)
        return unicode(self)

    def get_partner_instance(self):
        return self  # compatibility with lino.modlib.partners

    @dd.displayfield()
    def overview(self, ar):
        return E.div(*self.get_overview_elems(ar))

    def get_overview_elems(self, ar):
        elems = []
        buttons = self.get_mti_buttons(ar)
        # buttons = join_elems(buttons, ', ')
        elems.append(E.p(unicode(_("See as ")), *buttons,
                         style="font-size:8px;text-align:right;padding:3pt;"))
        elems += self.get_name_elems(ar)
        elems.append(E.br())
        elems += join_elems(list(self.address_location_lines()), sep=E.br)
        elems = [
            E.div(*elems,
                  style="font-size:18px;font-weigth:bold;"
                  "vertical-align:bottom;text-align:middle")]
        return elems

    def get_name_elems(self, ar):
        return [E.b(self.name)]


class PartnerDetail(dd.FormLayout):

    main = """
    address_box:60 contact_box:30
    bottom_box
    """

    address_box = dd.Panel("""
    name_box
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """, label=_("Address"))

    contact_box = dd.Panel("""
    info_box
    email:40
    url
    phone
    gsm fax
    """, label=_("Contact"))

    bottom_box = """
    remarks
    is_person is_company #is_user
    """

    name_box = "name"
    info_box = "id language"


class Partners(dd.Table):
    required = dd.Required(user_level='user')  # user_groups='office')
    model = 'contacts.Partner'
    column_names = "name email * id"
    order_by = ['name', 'id']
    #~ column_names = "name * id"
    detail_layout = PartnerDetail()
    insert_layout = dd.FormLayout("""
    name
    language email
    """, window_size=(40, 'auto'))

    @classmethod
    def get_queryset(self, ar):
        return self.model.objects.select_related('country', 'city')


#~ class AllPartners(Partners):

    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return _("All %s") % self.model._meta.verbose_name_plural

class PartnersByCity(Partners):
    master_key = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "street street_no street_box addr2 name language *"


class PartnersByCountry(Partners):
    master_key = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()


class Person(mixins.Human, mixins.Born, Partner):
    """
    A physical person and an individual human being.
    See :ref:`lino.tutorial.human`.

    """
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Person')
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        ordering = ['last_name', 'first_name']

    title = models.CharField(
        max_length=200, blank=True,
        verbose_name=_('Title'),
        help_text=_(
            "Text to print before allocation and name as part "
            "of the first address line."))

    def full_clean(self, *args, **kw):
        """Set the `name` field of this person.  This field is visible in the
        Partner's detail but not in the Person's detail and serves for
        sorting when selecting a Partner.  It also serves for quick
        search on Persons.

        """
        name = join_words(self.last_name, self.first_name)
        if name:
            self.name = name
        else:
            for k, v in name2kw(self.name).items():
                setattr(self, k, v)
            # self.last_name = self.name
        super(Person, self).full_clean(*args, **kw)

    def address_person_lines(self, *args, **kw):
        "Deserves more documentation."
        if self.title:
            yield self.title
        yield self.get_full_name(*args, **kw)
        #~ l = filter(lambda x:x,[self.first_name,self.last_name])
        #~ yield  " ".join(l)

    def get_name_elems(self, ar):
        elems = [self.get_salutation(nominative=True), E.br()]
        if self.title:
            elems += [self.title, ' ']
        elems += [self.first_name, ' ',
                  E.b(self.last_name)]
        return elems


class PersonDetail(PartnerDetail):

    name_box = "last_name first_name:15 gender title:10"
    info_box = "id:5 language:10"
    bottom_box = "remarks contacts.RolesByPerson"


class Persons(Partners):

    """
    List of all Persons.
    """
    #~ required = dict(user_level='user')
    model = "contacts.Person"
    order_by = ["last_name", "first_name", "id"]
    column_names = (
        "name_column:20 address_column email "
        "phone:10 gsm:10 id language:10 *")
    detail_layout = PersonDetail()

    insert_layout = dd.FormLayout("""
    first_name last_name
    gender language
    """, window_size=(60, 'auto'))


class CompanyType(mixins.BabelNamed):
    """A type of organization. Used by :attr:`Company.type` field.

    """
    class Meta:
        verbose_name = _("Organization type")
        verbose_name_plural = _("Organization types")

    abbr = dd.BabelCharField(_("Abbreviation"), max_length=30, blank=True)


class CompanyTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = 'contacts.CompanyType'
    column_names = 'name *'
    #~ label = _("Company types")


class Company(Partner):
    """An organisation.  The internal name is "Company" for historical
    reasons and because that's easier to type.

    See also :srcref:`docs/tickets/14`.

  .. attribute:: type
    
    Pointer to the :class:`CompanyType`.

    """
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Company')
        app_label = 'contacts'
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    prefix = models.CharField(
        _("Name prefix"), max_length=200, blank=True)

    type = models.ForeignKey('contacts.CompanyType', blank=True, null=True)

    def get_full_name(self, salutation=True, **salutation_options):
        """Deserves more documentation."""
        #~ print '20120729 Company.get_full_name`'
        if self.type:
            return join_words(self.prefix, self.type.abbr, self.name)
        return join_words(self.prefix, self.name)
    full_name = property(get_full_name)

    def get_name_elems(self, ar):
        elems = []
        if self.prefix:
            elems += [self.prefix, ' ']
        elems += [E.b(self.name)]
        return elems


class CompanyDetail(PartnerDetail):

    bottom_box = """
    remarks contacts.RolesByCompany
    """

    name_box = "prefix:10 name type:30"


class Companies(Partners):
    model = "contacts.Company"
    order_by = ["name"]
    column_names = (
        "name_column:20 address_column email "
        "phone:10 gsm:10 id language:10 *")
    detail_layout = CompanyDetail()
    insert_layout = dd.FormLayout("""
    name
    language:20 email:40
    type id
    """, window_size=(60, 'auto'))

#~ class List(Partner):
    #~ pass

#~ class Lists(Partners):
    #~ model = List
    #~ order_by = ["name"]
    #~ detail_layout = """
    #~ id name
    #~ language email
    #~ MembersByList
    #~ """
    #~ insert_layout = dd.FormLayout("""
    #~ name
    #~ language email
    #~ """,window_size=(40,'auto'))


# class ContactType(mixins.BabelNamed):
class RoleType(mixins.BabelNamed):

    """A :class:`RoleType` is "what a given :class:`Person` can be for a
    given :class:`Company`".

    TODO: rename "RoleType" to "Function" or "ContactType".
    
    RoleType,name is used at "in seiner Eigenschaft als ..."  in
    document templates for contracts.

    """
    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")


class RoleTypes(dd.Table):
    required = dd.required(user_level='manager')
    model = RoleType


#~ class Contact(dd.Model):
class Role(dd.Model, Addressable):

    """A Contact (historical model name :class:`Role`) is a
    :class:`Person` who has a given role (:class:`ContactType`) in a
    given :class:`Company`.
    
    """

    class Meta:
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")

    type = models.ForeignKey(
        'contacts.RoleType',
        blank=True, null=True,
        verbose_name=_("Contact Role"))
    person = models.ForeignKey(
        "contacts.Person", related_name='rolesbyperson')
    company = models.ForeignKey(
        "contacts.Company", related_name='rolesbycompany')

    def __unicode__(self):
        if self.person_id is None:
            return super(Role, self).__unicode__()
        if self.type is None:
            return unicode(self.person)
        return u"%s (%s)" % (self.person, self.type)

    def address_person_lines(self):
        if self.company:
            for ln in self.company.address_person_lines():
                yield ln
        for ln in self.person.address_person_lines():
            yield ln

    def address_location_lines(self):
        if self.company:
            return self.company.address_location_lines()
        else:
            return self.person.address_location_lines()


class Roles(dd.Table):
    required = dd.required(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = 'contacts.Role'


class RolesByCompany(Roles):
    required = dd.required()
    auto_fit_column_widths = True
    #~ required_user_level = None
    label = _("Contact persons")
    master_key = 'company'
    column_names = 'person type *'
    hidden_columns = 'id'


class RolesByPerson(Roles):
    required = dd.required()
    #~ required_user_level = None
    label = _("Contact for")
    master_key = 'person'
    column_names = 'company type *'
    auto_fit_column_widths = True
    hidden_columns = 'id'

dd.inject_field(
    'system.SiteConfig',
    'next_partner_id',
    models.IntegerField(
        default=PARTNER_NUMBERS_START_AT,
        blank=True, null=True,
        verbose_name=_("Next partner id"),
        help_text=_("The next automatic id for any new partner.")))

dd.inject_field(
    'system.SiteConfig',
    'site_company',
    models.ForeignKey(
        "contacts.Company",
        blank=True, null=True,
        verbose_name=_("Site owner"),
        related_name='site_company_sites',
        help_text=_("""The organisation who runs this site.
        This is used e.g. as sender in documents.
        Or, newly created partners inherit the country of the site owner.
        """)))


#~ dd.inject_field(Partner,
    #~ 'is_person',
    #~ mti.EnableChild(
        #~ settings.SITE.person_model,
        #~ verbose_name=_("is Person"),
        #~ help_text=_("Whether this Partner is a Person.")))
#~ dd.inject_field(Partner,
    #~ 'is_company',
    #~ mti.EnableChild(
        #~ "contacts.Company",
        #~ verbose_name=_("is Company"),
        #~ help_text=_("Whether this Partner is a Company.")))


def site_setup(site):

    site.modules.countries.Places.set_detail_layout("""
    name country
    type parent zip_code id
    PlacesByPlace
    contacts.PartnersByCity
    """)


@dd.receiver(dd.pre_analyze)
def company_model_alias(sender, **kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisation = sender.modules.contacts.Company


@dd.receiver(dd.post_analyze)
def company_tables_alias(sender, **kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisations = sender.modules.contacts.Companies


def PartnerField(**kw):
    return models.ForeignKey(Partner, **kw)
