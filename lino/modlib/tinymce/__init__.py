# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds usage of the TinyMCE editor
instead of Ext.form.HtmlEditor
for RichTextFields.
See also :attr:`tinymce_root`.
See `/blog/2011/0523`.
(formerly `use_tinymce`).

"""

from lino.api import ad


def javascript(url):
    return '<script type="text/javascript" src="{0}"></script>'.format(url)


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    needs_plugins = ['lino.modlib.office']  # because of TextFieldTemplate

    site_js_snippets = ['tinymce/tinymce.js']

    url_prefix = 'tinymce'

    media_name = 'tinymce-3.4.8'

    media_root = None
    # media_base_url = "http://www.tinymce.com/js/tinymce/jscripts/tiny_mce/"

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("TinyMCE", '3.4.8', "http://www.tinymce.com/")
            yield ("Ext.ux.TinyMCE", '0.8.4', "http://twitter.com/xorets")

    def get_js_includes(self, settings, language):
        yield self.build_lib_url('tiny_mce.js')
        yield settings.SITE.build_static_url("tinymce/Ext.ux.TinyMCE.js")

    def get_head_lines(self, site, request):
        # yield javascript(site.build_media_url("tinymce", "tiny_mce.js"))
        # yield javascript(site.build_media_url(
        #     "lino", "tinymce", "Ext.ux.TinyMCE.js"))
        yield """
<script language="javascript" type="text/javascript">
    tinymce.init({
            theme : "advanced"
            // , mode : "textareas"
    });
</script>"""

    def get_patterns(self, kernel):
        from django.conf.urls import url
        from . import views

        rx = '^'

        urlpatterns = [
            url(rx + r'templates/(?P<app_label>\w+)/'
                + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)$',
                views.Templates.as_view()),
            url(rx + r'templates/(?P<app_label>\w+)/'
                + r'(?P<actor>\w+)/(?P<pk>\w+)/(?P<fldname>\w+)/'
                + r'(?P<tplname>\w+)$',
                views.Templates.as_view())]

        return urlpatterns

    def get_row_edit_lines(self, e, panel):
        from lino.modlib.extjs.elems import TextFieldElement
        if isinstance(e, TextFieldElement):
            if e.format == 'html':
                yield "%s.refresh();" % e.as_ext()

    def setup_config_menu(self, site, profile, m):
        if site.user_model is not None:
            mg = site.plugins.office
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('tinymce.MyTextFieldTemplates')

    def setup_explorer_menu(self, site, profile, m):
        if site.user_model is not None:
            mg = site.plugins.office
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('tinymce.TextFieldTemplates')


