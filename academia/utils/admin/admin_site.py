from django.contrib.admin import AdminSite
import json
from academia.utils.admin.generic_admin import GenericAdmin
from django.contrib import admin

class CustomAdminSite(AdminSite):

    def get_superuser_access_apps(self):
        return ['auditlog']
    
    def get_app_list(self, request):
        app_list = super(CustomAdminSite, self).get_app_list(request)
        if not app_list:
            return []
        superuser_access_apps = self.get_superuser_access_apps()
        if not request.user.is_superuser:
            app_list = list(filter(lambda app: app['app_label'] not in superuser_access_apps, app_list))
        from django.apps import apps
        for idx, app in enumerate(app_list):
            config = apps.get_app_config(app['app_label'])
            if hasattr(config, 'icon'):
                app_list[idx]['icon'] = config.icon
            else:
                app_list[idx]['icon'] = 'fa fa-home'
        return app_list
    
    