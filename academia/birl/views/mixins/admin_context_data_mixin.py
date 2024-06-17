import json

from django.contrib.auth import get_permission_codename
from django.views.generic.base import ContextMixin
from django.contrib import admin


class AdminContextDataMixin(ContextMixin):
    request = None
    object = None
    save_as = False
    has_editable_inline_admin_formsets = False
    model_to_check_permission = None

    def get_extra_context(self) -> dict:
        return {}

    def get_js_context(self) -> dict:
        return {}

    def get_context_data(self, **kwargs) -> dict:
        ctx = super(AdminContextDataMixin, self).get_context_data(**kwargs)
        ctx.update(admin.site.each_context(self.request))
        if self.object:
            ctx['opts'] = self.object._meta
        ctx.update({
            'js_context': json.dumps(self.get_js_context())
        })
        ctx.update({
            'title': self.object._meta.verbose_name if self.object else '',
            'subtitle': str(self.object) if self.object else '',
            'object_id': self.object.id if self.object else None,
            'original': self.object,
            'add': self.object and not self.object.id,
            'save_as': self.save_as,
            'change': self.object and self.object.id,
            'has_view_permission': self.has_view_permission(self.object or self.model_to_check_permission),
            'has_add_permission': self.has_add_permission(self.object or self.model_to_check_permission),
            'has_change_permission': self.has_change_permission(self.object or self.model_to_check_permission),
            'has_delete_permission': self.has_delete_permission(self.object or self.model_to_check_permission),
            'opts': self.get_opts(),
            'has_editable_inline_admin_formsets': self.has_editable_inline_admin_formsets,
            **self.get_extra_context(),
        })
        return ctx

    def has_add_permission(self, obj) -> bool:
        codename = get_permission_codename('add', obj._meta)
        return self.request.user.has_perm("%s.%s" % (obj._meta.app_label, codename))

    def has_change_permission(self, obj=None) -> bool:
        codename = get_permission_codename('change', obj._meta)
        return self.request.user.has_perm("%s.%s" % (obj._meta.app_label, codename))

    def has_delete_permission(self, obj=None) -> bool:
        codename = get_permission_codename('delete', obj._meta)
        return self.request.user.has_perm("%s.%s" % (obj._meta.app_label, codename))

    def has_view_permission(self, obj=None) -> bool:
        codename_view = get_permission_codename('view', obj._meta)
        codename_change = get_permission_codename('change', obj._meta)
        return (
                self.request.user.has_perm('%s.%s' % (obj._meta.app_label, codename_view)) or
                self.request.user.has_perm('%s.%s' % (obj._meta.app_label, codename_change))
        )

    def get_model_perms(self) -> dict:
        return {
            'add': self.has_add_permission(self.request),
            'change': self.has_change_permission(self.request),
            'delete': self.has_delete_permission(self.request),
            'view': self.has_view_permission(self.request),
        }

    def get_opts(self) -> object:
        if self.object:
            return self.object._meta
        if self.model_to_check_permission:
            return self.model_to_check_permission._meta
        return None
