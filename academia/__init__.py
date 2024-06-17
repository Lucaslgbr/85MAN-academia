from django.contrib.admin import sites
from django.contrib import admin

from academia.utils.admin.admin_site import CustomAdminSite


site = CustomAdminSite()
admin.site = site
admin.site.disable_action('delete_selected')
sites.site = site

__version__ = '1.0.0'

def get_version():
    return __version__