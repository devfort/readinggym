from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def include_css(context, *names, **options):
    assets = context['assets']
    return mark_safe(assets.include_css(*names, **options))

@register.simple_tag(takes_context=True)
def include_image(context, *names, **options):
    assets = context['assets']
    return mark_safe(assets.include_image(*names, **options))

@register.simple_tag(takes_context=True)
def include_js(context, *names, **options):
    assets = context['assets']
    return mark_safe(assets.include_js(*names, **options))
