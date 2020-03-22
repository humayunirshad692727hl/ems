from django import template
from poll.models import Question

register = template.Library()

def upper(value, n):
    """Converts a string into all uppercase"""
    return value.upper()[0:n]

register.filter('upper', upper)#it defines that if we use the first upper then the actual upper function will be called
#to register tag use register.tag()


@register.simple_tag## we can use either this method or the above method to register the tag @register.simple_tag(name='any name') it also takes name to use it instaed of function name 
def recent_polls(n=5, **kwargs):
    """Return recent n polls"""
    name = kwargs.get("name", "Argument is not passed")
    print(name)
    questions = Question.objects.all().order_by('-created_at')
    return questions[0:n]