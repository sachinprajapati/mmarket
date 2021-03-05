from django import template

register = template.Library()

@register.simple_tag
def get_breadcrumb(path):
    return ' > '.join(path[1:-1].split('/')).title()

@register.simple_tag
def field_type(type):
    if type=='integer':
        return 'number'


@register.simple_tag
def AtrributeValue(a):
    value = 'value_'+a.attribute.type
    return getattr(a, value)
