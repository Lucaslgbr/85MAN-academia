from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django import forms
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from academia.utils.admin.generic_admin import GenericAdmin
from django.contrib.auth.forms import UserCreationForm as AdminUserCreationForm
from django.contrib.auth.forms import UserChangeForm as AdminUserUpdateForm
from academia.birl.consts.groups import DefaultGroups

# from import_export.admin import ExportMixin
class UsuarioAdmin(GenericAdmin, UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter=['is_active']
    add_form=AdminUserCreationForm
    form=AdminUserUpdateForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj,  **kwargs)
        return form

    fieldsets = (
        (None, {"fields": ("username",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'groups')}),
        (
            _("Permissions"),
            {
                "fields": [
                ],
            },
        ),
    )
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name", "last_name", "groups", "password1", "password2"),
            },
        ),
        
    )
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        request.POST._mutable = True
        if request.POST:
            if 'groups' in request.POST:
                request.POST['groups'] = Group.objects.filter(id=request.POST['groups'])
    
        form = super(UsuarioAdmin, self).get_form(request, obj, change, **kwargs)

        form.base_fields['first_name'].required = True
        if 'projects' in form.base_fields:
            form.base_fields['projects'].required = False


        if 'user_permissions' in form.base_fields:
            form.base_fields['user_permissions'] = forms.HiddenInput()
        if 'password' in form.base_fields:
            form.base_fields['password'].widget = forms.HiddenInput()
        if 'groups' in form.base_fields:
            form.base_fields['groups'].widget = forms.RadioSelect()
            exclude_groups = []
            if not request.user.is_superuser:
                exclude_groups.append(DefaultGroups.ADMINISTRATOR)
            form.base_fields['groups'].queryset = Group.objects.exclude(
                name__in=exclude_groups)
        return form
    
    def get_fieldsets(self, request, obj,*args, **kwargs):
        if not obj:
            return super().get_fieldsets(request, obj,*args, **kwargs)
        if obj.is_superuser:
            self.fieldsets[2][1]['fields']= [
                    "password",
                    "is_active",
                    "is_superuser",
                    "groups"
                ]
        else:
             self.fieldsets[2][1]['fields']= [
                    "password",
                    "is_active",
                    "is_superuser",
                ]
        return super().get_fieldsets(request, obj,*args, **kwargs)
    
admin.site.register(get_user_model(), UsuarioAdmin)
