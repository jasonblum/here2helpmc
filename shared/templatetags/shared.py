import pendulum
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter()
def htmlattributes(value, arg):
    attrs = value.field.widget.attrs

    kvs = arg.split(',')

    for string in kvs:
        kv = string.split(':')
        attrs[kv[0]] = kv[1]

    rendered = str(value)

    return rendered


@register.filter()
def friendly_date(date):
    date_as_string = date.strftime('%A %B %d')
    if date.date() == pendulum.now().date():
        date_as_string = f'Today {date_as_string}'
    elif date.date() == pendulum.now().add(days=1).date():
        date_as_string = f'Tomorrow {date_as_string}'

    return date_as_string