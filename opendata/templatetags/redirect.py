from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='redirect')
@stringfilter
def redirect(file_url):
    return file_url.replace('/static/', '/redirect/')
