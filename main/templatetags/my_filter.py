from django import template
register = template.Library()


def two_digits(num):
    if 0 < num < 10:
        return '0' + str(num)
    else:
        return str(num)


register.filter(two_digits)
