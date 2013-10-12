from django.conf import settings

def analytics(request):
    return {
        'GA_ACCOUNT_ID': getattr(settings, 'GA_ACCOUNT_ID', ''),
        'GA_HOSTNAME': getattr(settings, 'GA_HOSTNAME', '')
    }
