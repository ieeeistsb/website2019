from app.models import Community, Projects, SocialNetwork, News
from django import template

register = template.Library()


@register.simple_tag
def get_all_communities():
    return Community.objects.all()


@register.simple_tag
def get_all_projects():
    return Projects.objects.all()


@register.simple_tag
def get_branch_socials():
    return SocialNetwork.objects.filter(is_from_branch=True)


@register.simple_tag
def get_latest_news():
    objs = News.objects.all().order_by("-date")
    if len(objs) > 5:
        return objs[0:5]
    return objs
