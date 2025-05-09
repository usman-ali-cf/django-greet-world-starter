from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Filter to access dictionary values by key in templates"""
    return dictionary.get(key)

