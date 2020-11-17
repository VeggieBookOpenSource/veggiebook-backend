from django import template
import math

register = template.Library()

@register.filter("firsthalf", is_safe=True)
def firsthalf_filter(value):
    """
Returns firsthalf of the list, rounded up if needed.
"""
    try:
        return value[0:int(math.ceil(len(value)/2.0))] 
    except (ValueError, TypeError):
        return value # Fail silently.

@register.filter("secondhalf", is_safe=True)
def secondhalf_filter(value):
    """
Returns secondhalf of the list, rounded down if needed.
"""
    try:
        return value[int(math.ceil(len(value)/2.0)):] 
    except (ValueError, TypeError):
        return value # Fail silently.

@register.filter("add1ThenTimes4", is_safe=True)
def add1Times4_filter(n):
    """
    Returns (n+1)*4
    :param n: input integer
    """
    try:
        return (n+1)*4
    except:
        return n

@register.filter("timesOnePoint2", is_safe=True)
def otopt(n):
    try:
        return n * .6
    except:
        return n
