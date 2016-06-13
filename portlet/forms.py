# -*- coding: utf-8 -*-
from django import forms
from ajax_select.fields import AutoCompleteField

from portlet.models import Portlet

class PortletAdminForm(forms.ModelForm):
    display_title_link = AutoCompleteField('pages', required=False)

    class Meta:
        model = Portlet
        fields = '__all__'
