from django import template

register = template.Library()


@register.filter(name='check_evaluated')
def check_evaluated(userSolution, user):

    return userSolution.evaluated.filter(whoEvaluated=user).exists()  # check if relationship exists


@register.filter(name='get_obj_attr')
def get_obj_attr(obj, field):
    return getattr(obj, field)


@register.simple_tag
def get_verbose_name(thing):
    return thing.verbose_name


@register.filter(name='returnIndex')
def returnIndex(queryset, index):
    newList = list(queryset)
    return newList.index(index) + 1


@register.filter(name='nextExpo')
def nextExpo(queryset, nextValue):
    newList = list(queryset)
    nextChallenge = newList.index(nextValue)+1
    print(nextValue.id)
    return newList[nextChallenge].learningexperience_set.first().pk




