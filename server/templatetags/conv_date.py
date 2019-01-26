from datetime import datetime

from django import template

register = template.Library()

@register.filter(name='conv_date')
def __convert_date(date):
    return str(date).replace('T', ' ').replace('Z', ' ').split('.')[0]
