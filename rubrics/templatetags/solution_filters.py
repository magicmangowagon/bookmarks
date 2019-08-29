from django import template

register = template.Library()


@register.filter(name='check_evaluated')
def check_evaluated(userSolution, user):

    return userSolution.evaluated.filter(whoEvaluated=user).exists() # check if relationship exists


@register.filter(name='get_verbose_name')
def get_item(object, field):
    verbose_name = object._meta.get_field(field).verbose_name
    return verbose_name
