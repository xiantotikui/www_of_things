from django import template

register = template.Library()

@register.filter(name='add_units')
def __add_units(name, val_type):
    if val_type == 'DS18B20':
        return str(name) + '°C'
    else:
        return name
