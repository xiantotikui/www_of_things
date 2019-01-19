from datetime import datetime

from django import template

register = template.Library()

@register.filter(name='conv_date')
def __convert_date(date):
    tmp = datetime.strptime(date[:-5], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    return tmp
