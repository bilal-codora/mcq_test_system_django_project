from django import template

register = template.Library()


@register.filter
def get_option_text(question, option_number):
    return getattr(question, f'option{option_number}', 'Invalid option')