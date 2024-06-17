import json
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.urls import reverse,path
from django.utils.html import format_html
import json
from django.contrib.admin import helpers
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.utils import (
    flatten_fieldsets,
    unquote,
)
from crispy_forms.helper import FormHelper
from django.core.exceptions import (
    PermissionDenied,
)
from django.forms.formsets import  all_valid
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.admin.options import TO_FIELD_VAR, IS_POPUP_VAR
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

# from academia.utils.queryset import get_queryset


class GenericAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 10
    include_action_column=True
    instance=None
    detail_template = 'admin/detail/object_detail.html' 
    save_as = False
        
    def has_view_history_permission(self, request):
        return True
    
    def get_form_class(self,request):
        return self.form
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        if self.model._meta.model_name == 'usuario':
            form = super(GenericAdmin, self).get_form(request, obj, **kwargs)
        else:
            form = super(GenericAdmin, self).get_form(request, obj, change, **kwargs)
        form.helper = FormHelper()
        form.helper.include_media = False
        extra_attrs=self.get_form_extra_attrs(request)
        return form
    
    def get_urls(self):
        info = self.opts.app_label, self.opts.model_name
        return [
            path(
                "<path:object_id>/detail/",
                self.admin_site.admin_view(self.detail_view),
                name="%s_%s_detail" % info,
            ),
            *super(GenericAdmin,self).get_urls()
        ]
    
    def _detail_view(self,request,instance,extra_context={}):
        extra_context = {}
        extra_context.update({
            **self.admin_site.each_context(request),
            'object':self.instance,
            'opts':self.opts,
            'module_name':str(self.opts.verbose_name_plural),
            'back_button_href':request.META.get('HTTP_REFERER'),
            'js_context': json.dumps(self.get_detail_js_context(request)),
            **self.get_detail_extra_context(request),
        })
        return TemplateResponse(request,self.detail_template,extra_context)
    
    def detail_view(self,request,object_id,extra_context={}):
        self.instance =  get_object_or_404(self.model, pk=object_id)
        self.instance =  get_object_or_404(self.model, pk=object_id)
        # if self.instance not in self.get_queryset(request):
        #     return HttpResponseForbidden()
        return self._detail_view(request,self.instance,extra_context)

    def get_object_tools(self,request):
        return []

    def get_extra_forms(self,request)->dict:
        return {}
    
    # def get_queryset(self, request):
        # return get_queryset(seGenericAdminlf.model, request, super().get_queryset, request)
    
    def get_list_display(self,request):
        display = list(super().get_list_display(request))
        if hasattr(self.model,'admin_list_display'):
            display = [*self.model.admin_list_display]
        if self.include_action_column:
            display.append('action_column')
        return display
            
    def get_form_extra_attrs(self,request)->dict:
        return {}

    def get_form_extra_context(self, request):
        return {}
    
    def get_detail_extra_context(self, request):
        return {}

    def get_list_extra_context(self, request):
        return {}

    def get_form_js_context(self, request):
        return {}
    
    def get_detail_js_context(self, request):
        return {}
    
    def get_list_js_context(self, request):
        return {}
    
    def add_view(self, request, form_url="", extra_context=None):
        self.instance=None
        return self.changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.user=request.user
        self.request=request
        self.instance = self.model.objects.get(id=object_id)
        # if self.instance not in self.get_queryset(request):
        return super().change_view(request,object_id,form_url,extra_context)
    
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            **self.get_form_extra_context(request), 
            'extra_forms':self.get_extra_forms(request),
            'js_context': json.dumps(self.get_form_js_context(request)),
            'back_button_href':request.META.get('HTTP_REFERER'),
            'show_delete':False
            })
        return super(GenericAdmin, self).changeform_view(request, object_id, form_url, extra_context)
    
    def validate_extra_forms(self,extra_forms):
        for key,form_instance in extra_forms.items():
            if not form_instance.is_valid():
                return False
        return True
    
    def save_extra_forms(self,extra_forms,parent_instance):
        for key,form_instance in extra_forms.items():
            form_instance.save()
    
    # def parse_query_params(self, request):
    #     removeable_keys = []
    #     for k,v in request.GET.items():
    #         if not v:
    #             removeable_keys.append(k)
    #     if removeable_keys:
    #         request.GET._mutable=True
    #     for key in  removeable_keys:
    #         del request.GET[key]  
    #     return request

    
    def changelist_view(self, request, extra_context=None):
        from django.contrib.contenttypes.models import ContentType  
        # request = self.parse_query_params(request)
        self.user=request.user
        self.request=request
        extra_context = extra_context or {}
        extra_context.update({
            **self.get_list_extra_context(request),
             'js_context': self.get_list_js_context(request),
             'object_tools':self.get_object_tools(request),
        })
        return super(GenericAdmin, self).changelist_view(request, extra_context)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def render_action_link(self,href,title='',icon='',onclick='',icon_size=2, target=None):
        if target:
            return f"<a target={target} href={href} onclick={onclick}><i title='{title}' class ='fa fa-{icon_size}x {icon} ml-2'></i></a>"
        return f"<a href={href} onclick={onclick}><i title='{title}' class ='fa fa-{icon_size}x {icon} ml-2'></i></a>"
    
    def get_action_links(self,obj):
        '''Override this method to add extra links'''
        return []
    
    def get_change_action_link(self,obj):
        return self.render_action_link(reverse(
                f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args={obj.id}), 'Editar', 'fa fa-edit fa-2x', 2)
    
    @admin.display(description='Ações')
    def action_column(self, obj):
        action_links = self.get_action_links(obj)
        if self.has_change_permission(self.request,obj):
            action_links.append(self.get_change_action_link(obj))
        if self.has_view_history_permission(self.request):
            history_button = self.render_action_link(reverse(
                f"admin:{obj._meta.app_label}_{obj._meta.model_name}_history", args={obj.id}), 'Histórico', 'fa fa-eye fa-2x', 2)
            action_links.append(history_button)
        return format_html(''.join(action_links))
    
    
    def _changeform_view(self, request, object_id, form_url, extra_context):
        # 99% of this method is a copy/paste from the parent admin. We had to do this to add a feature to validate extra forms 
        # its a diffrent aproach of how admin handles the  AdminForm and the inlines 

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField(
                "The field %s cannot be referenced." % to_field
            )

        if request.method == "POST" and "_saveasnew" in request.POST:
            object_id = None

        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if request.method == "POST":
                if not self.has_change_permission(request, obj):
                    raise PermissionDenied
            else:
                if not self.has_view_or_change_permission(request, obj):
                    raise PermissionDenied

            if obj is None:
                return self._get_obj_does_not_exist_redirect(
                    request, self.opts, object_id
                )

        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(
            request, obj, change=not add, fields=flatten_fieldsets(fieldsets)
        )
        if request.method == "POST":
            form = ModelForm(request.POST, request.FILES, instance=obj,**self.get_form_extra_attrs(request))
            formsets, inline_instances = self._create_formsets(
                request,
                form.instance,
                change=not add,
            )
            form_validated = form.is_valid()
            if form_validated:
                new_object = self.save_form(request, form, change=not add)
            else:
                new_object = form.instance

            extra_forms = self.get_extra_forms(request)
            extra_forms_valid = self.validate_extra_forms(extra_forms)
            
            if all_valid(formsets) and form_validated and extra_forms_valid:
                self.save_extra_forms(extra_forms,new_object)
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                change_message = self.construct_change_message(
                    request, form, formsets, add
                )
                if add:
                    self.log_addition(request, new_object, change_message)
                    return self.response_add(request, new_object)
                else:
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
            else:
                form_validated = False
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial,**self.get_form_extra_attrs(request))
                formsets, inline_instances = self._create_formsets(
                    request, form.instance, change=False
                )
            else:
                form = ModelForm(instance=obj,**self.get_form_extra_attrs(request))
                formsets, inline_instances = self._create_formsets(
                    request, obj, change=True
                )

        if not add and not self.has_change_permission(request, obj):
            readonly_fields = flatten_fieldsets(fieldsets)
        else:
            readonly_fields = self.get_readonly_fields(request, obj)
        admin_form = helpers.AdminForm(
            form,
            list(fieldsets),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            self.get_prepopulated_fields(request, obj)
            if add or self.has_change_permission(request, obj)
            else {},
            readonly_fields,
            model_admin=self,
        )
        media = self.media + admin_form.media

        inline_formsets = self.get_inline_formsets(
            request, formsets, inline_instances, obj
        )
        for inline_formset in inline_formsets:
            media += inline_formset.media

        if add:
            title = _("Add %s")
        elif self.has_change_permission(request, obj):
            title = _("Change %s")
        else:
            title = _("View %s")
        context = {
            **self.admin_site.each_context(request),
            "title": title % self.opts.verbose_name,
            "subtitle": str(obj) if obj else None,
            "adminform": admin_form,
            "object_id": object_id,
            "original": obj,
            "is_popup": IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            "to_field": to_field,
            "media": media,
            "inline_admin_formsets": inline_formsets,
            "errors": helpers.AdminErrorList(form, formsets),
            "preserved_filters": self.get_preserved_filters(request),
        }

        # Hide the "Save" and "Save and continue" buttons if "Save as New" was
        # previously chosen to prevent the interface from getting confusing.
        context["show_save_and_continue"] = False
        context["show_save_and_add_another"] = False
            
        if (
            request.method == "POST"
            and not form_validated
            and "_saveasnew" in request.POST
        ):
            context["show_save"] = False
            context["show_save_and_continue"] = False
            # Use the change template instead of the add template.
            add = False

        context.update(extra_context or {})

        return self.render_change_form(
            request, context, add=add, change=not add, obj=obj, form_url=form_url
        )

   