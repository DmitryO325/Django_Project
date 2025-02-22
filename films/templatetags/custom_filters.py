from django import template

register = template.Library()


@register.filter
def _range(value):
    return range(1, value + 1)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)
