from django.views.generic.base import ContextMixin
from rest_framework.authtoken.models import Token

from academia.birl.api.v1.api_router import router


class APIUrlsContextMixin(ContextMixin):
    request = None

    def get_context_data(self, **kwargs):
        ctx = super(APIUrlsContextMixin, self).get_context_data(**kwargs)
        api_urls = {}
        for route in router.available_routes:
            api_urls[route['model'].upper()] = f"/api/v1/{route['model']}/"
        ctx.update({
            'api_urls': api_urls,
            'authtoken':Token.objects.get_or_create(user=self.request.user)[0].key
        })
        return ctx
