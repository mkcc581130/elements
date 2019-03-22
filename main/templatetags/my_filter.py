from django import template
register = template.Library()


def two_digits(num):
    if 0 < num < 10:
        return '0' + str(num)
    else:
        return str(num)


def digits(flo, num=2):
    if isinstance(num, int):
        try:
            flo.index('.')
            return round(float(flo.replace(' ', '')), num)
        except ValueError:
            return flo


register.filter(two_digits)
register.filter(digits)
