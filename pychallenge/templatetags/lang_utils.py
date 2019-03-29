from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get active page's url by a specified language
        Usage: {% change_lang 'en' %}
    """

    path = context['request'].path
    return "/%s%s" % (lang, path[3:])
