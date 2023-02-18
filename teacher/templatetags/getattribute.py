import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()
from branch.models import branch_detail
def getattribute(value, arg):
    arg=str(arg)
    """Gets an attribute of an object dynamically from a string name"""
    print(isinstance(value,branch_detail),111111111111111111)
    print(getattr(value,'tues_lec1'),arg)
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return 1

register.filter('getattribute', getattribute)

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)