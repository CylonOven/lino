# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
.. autosummary::

"""

from django.utils.functional import Promise
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino.core import actions
from lino.core import choicelists


class State(choicelists.Choice):
    """A `State` is a specialized :class:`Choice
    <lino.core.choicelists.Choice>` that adds the
    :meth:`add_transition` method.

    """

    def add_transition(self, label=None,
                       help_text=None,
                       notify=False,
                       name=None,
                       #~ icon_file=None,
                       icon_name=None,
                       debug_permissions=None,
                       **required):
        """Declare or create a `ChangeStateAction` which makes the object
enter this state.  `label` can be either a string or a subclass of
ChangeStateAction.

        You can specify an explicit `name` in order to allow replacing
        the transition action later by another action.

        """
        workflow_actions = self.choicelist.workflow_actions
        i = len(workflow_actions)
        if name is None:
            #~ name = 'mark_' + self.value
            name = 'wf' + str(i + 1)
        
        for x in self.choicelist.workflow_actions:
            if x.action_name == name:
                raise Exception(
                    "Duplicate transition name {0}".format(name))
    
        kw = dict()
        if help_text is not None:
            kw.update(help_text=help_text)
        if icon_name is not None:
            kw.update(icon_name=icon_name)
        kw.update(sort_index=10 + i)
        if label and not isinstance(label, (basestring, Promise)):
            # it's a subclass of ChangeStateAction
            assert isinstance(label, type)
            assert issubclass(label, ChangeStateAction)
            if required:
                raise Exception(
                    "Cannot specify requirements when using your own class")
            if notify:
                raise Exception(
                    "Cannot specify notify=True when using your own class")
            if debug_permissions:
                raise Exception(
                    "Cannot specify debug_permissions "
                    "when using your own class")
            for a in workflow_actions:
                if isinstance(a, label):
                    raise Exception("Duplicate transition label %s" % a)
            a = label(self, required, **kw)
        else:
            if notify:
                cl = NotifyingChangeStateAction
            else:
                cl = ChangeStateAction
            a = cl(self, required, label=label or self.text, **kw)
            if debug_permissions:
                a.debug_permissions = debug_permissions
        a.attach_to_workflow(self.choicelist, name)

        self.choicelist.workflow_actions = workflow_actions + [a]

    add_workflow = add_transition  # backwards compat


class Workflow(choicelists.ChoiceList):

    """A Workflow is a specialized ChoiceList used for defining the
    states of a workflow.

    """
    item_class = State

    verbose_name = _("State")
    verbose_name_plural = _("States")

    @classmethod
    def on_analyze(cls, site):
        """Add workflow actions to the models using this workflow so that we
        can access them as InstanceActions.

        """
        super(Workflow, cls).on_analyze(site)
        for fld in cls._fields:
            model = getattr(fld, 'model', None)
            if model:
                for a in cls.workflow_actions:
                    if not a.action_name.startswith('wf'):
                        setattr(model, a.action_name, a)

    @classmethod
    def before_state_change(cls, obj, ar, oldstate, newstate):
        pass

    @classmethod
    def after_state_change(cls, obj, ar, oldstate, newstate):
        pass

    @classmethod
    def override_transition(cls, **kw):
        """
        """
        for name, cl in kw.items():
            found = False
            for i, a in enumerate(cls.workflow_actions):
                if a.action_name == name:
                    new = cl(
                        a.target_state, a.required, sort_index=a.sort_index)
                    new.attach_to_workflow(cls, name)
                    cls.workflow_actions[i] = new
                    found = True
                    break
            if not found:
                raise Exception(
                    "There is no workflow action named {0}".format(name))


class ChangeStateAction(actions.Action):

    """This is the class used when generating automatic "state
    actions". For each possible value of the Actor's
    :attr:`workflow_state_field` there will be an automatic action
    called `mark_XXX`

    """

    show_in_bbar = False
    show_in_workflow = True

    def __init__(self, target_state, required, help_text=None, **kw):
        self.target_state = target_state
        #~ kw.update(label=getattr(target_state,'action_label',target_state.text))
        #~ kw.setdefault('label',target_state.text)
        #~ required = getattr(target_state,'required',None)
        #~ if required is not None:
        assert not 'required' in kw
        new_required = dict(self.required)
        new_required.update(required)
        if target_state.name:

            m = getattr(target_state.choicelist, 'allow_transition', None)
            if m is not None:
                assert not 'allowed' in required

                def allow(action, user, obj, state):
                    return m(obj, user, target_state)
                new_required.update(allow=allow)

        kw.update(required=new_required)
        if self.help_text is None:
            if help_text is None:
                help_text = _("Mark this as %s") % target_state.text
        #~ help_text = getattr(target_state,'help_text',None)
        #~ if help_text is not None:
            kw.update(help_text=help_text)
        else:
            assert help_text is None

        super(ChangeStateAction, self).__init__(**kw)
        #~ logger.info('20120930 ChangeStateAction %s %s', actor,target_state)
        if self.icon_name:
            self.help_text = string_concat(self.label, '. ', self.help_text)

    def run_from_ui(self, ar):
        row = ar.selected_rows[0]
        self.execute(ar, row)
        ar.set_response(refresh=True)
        ar.success()

    def execute(self, ar, obj):
        return obj.set_workflow_state(
            ar,
            ar.actor.workflow_state_field,
            self.target_state)


class NotifyingChangeStateAction(ChangeStateAction, actions.NotifyingAction):
    pass
