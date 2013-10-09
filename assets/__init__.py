# assets/__init__.py

from django.conf import settings

class AssetsMiddleware:
    def process_request(self, request):
        request.assets = settings.WAKE_ASSETS.renderer()

def assets_context(request):
    return {'assets': request.assets}
