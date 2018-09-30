from django import template

register = template.Library()

@register.filter(name="splitpart")
def splitpart (value, index, char = '&page'):
    querystring = str(value).split(char)
    return querystring[index]
