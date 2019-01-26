from django import template

register = template.Library()

@register.filter(name='modify_name')
def __mod_name(name):
    if name == 'DS18B20':
        return 'Czujnik temperatury'
    else:
        return name
