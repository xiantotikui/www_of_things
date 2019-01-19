from django import template

register = template.Library()

@register.filter(name='is_mod')
def __is_moderator(user):
    return user.groups.filter(name='Mod').exists()
