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


def parse_int(string):
    return int(string)


def multiplication(number, multi):
    return int(number)*int(multi)


def type_of(name, type_name):
    name = str(name).strip()
    return name.endswith(type_name)


register.filter(two_digits)
register.filter(digits)
register.filter(parse_int)
register.filter(multiplication)
register.filter(type_of)
