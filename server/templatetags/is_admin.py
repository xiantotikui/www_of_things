from django import template

register = template.Library()

@register.filter(name='is_admin')
def __is_admin(user):
    return user.groups.filter(name='Admin').exists()
