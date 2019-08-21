from django import template

register = template.Library()


@register.filter(name='check_evaluated')
def check_evaluated(userSolution, user):

    return userSolution.evaluated.filter(whoEvaluated=user).exists() # check if relationship exists