# assets/__init__.py

from django.conf import settings
from ua_parser import user_agent_parser

MOBILES = ['iPhone', 'iPad', 'Kindle']

def is_mobile(request):
    user_agent = user_agent_parser.Parse(request.META['HTTP_USER_AGENT'])
    return user_agent['device']['family'] in MOBILES

class AssetsMiddleware:
    def process_request(self, request):
        options = {}
        if hasattr(settings, 'ASSET_HOSTS'):
            options['hosts'] = settings.ASSET_HOSTS
        if is_mobile(request):
            options['inline'] = True
        request.assets = settings.WAKE_ASSETS.renderer(**options)

def assets_context(request):
    return {'assets': request.assets}
