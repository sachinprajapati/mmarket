from django import template

register = template.Library()

@register.simple_tag
def get_breadcrumb(path):
    return ' > '.join(path[1:-1].split('/')).title()