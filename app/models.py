from __future__ import unicode_literals
from app.validators import validate_if_is_pdf_file

from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible
from django.db import models
import markdown
from django.utils.translation import get_language
import datetime
import os
from django.conf import settings


def load_translated_field(obj, field):
    if get_language() == "pt":
        field += "_pt"
    return getattr(obj, field)


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        reganha = os.name == "nt"

        if reganha:
            separator = "\\"
        else:
            separator = "/"

        filename = filename.split(separator)[-1]
        namesplit = filename.split('.')
        ext = namesplit[-1]
        date = datetime.datetime.now()
        name = "".join(namesplit[:-1])
        filename = name + "_" + date.strftime("%Y%m%d%H%M%S") + "." + ext
        return os.path.join(self.path, filename)


path_volunteers = PathAndRename("img/volunteers/")
path_communities = PathAndRename("img/communities/")
path_projects = PathAndRename("img/projects/")
path_news = PathAndRename("img/news/")
path_initiatives = PathAndRename("img/initiative_events/")
path_partners = PathAndRename("img/partners")
path_newsletters = PathAndRename("pdf/newsletters")


class TranslatableTitle(models.Model):
    title = models.CharField(max_length=100)
    title_pt = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

    @classmethod
    def get_equals(cls, query):
        """
        Returns query you need to make in order to search in both fields of this class. Use this method if you want to
        search for an EXACT entry in either field (case insensitive).
        :param query: string to search in database
        :return: query to use in django query methods (e.g. get, filter...)
        """
        return models.Q(title__iexact=query) | models.Q(title_pt__iexact=query)

    @classmethod
    def get_contains(cls, query):
        """
        Returns query you need to make in order to search in both fields of this class. Use this method if you want to
        search for an entry that contains given string in either field (case insensitive).
        :param query: string to search in database
        :return: query to use in django query methods (e.g. get, filter...)
        """
        return models.Q(title__icontains=query) | models.Q(title_pt__icontains=query)

    def get_title(self):
        return load_translated_field(self, 'title')

    class Meta:
        abstract = True


class TranslatableUniqueTitle(models.Model):
    """
        Guarantees unique titles. A slight performance penalty during inserts in exchange for guaranteed pretty URLs
        e.g.: https://[...]/initiative/collabs/ instead of https://[...]/initiative/2/
        Extend this abstract model if the following conditions hold:
        1. You want titles in URLs
        2. You don't expect frequent inserts in your table
        3. You don't expect to have millions of instances of your model

        TODO: This will behave badly if you create an object with title_pt attribute that is equal to some other
        object's of the same class title attribute.
        E.g. a = MyClass(title="foo", title_pt="bar") and b = MyClass(title="bar", title_pt="something")
    """
    title = models.CharField(max_length=100, unique=True)
    title_pt = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.title

    @classmethod
    def get_contains(cls, query):
        """
        Returns query you need to make in order to search in both fields of this class. Use this method if you want to
        search for an entry that contains given string in either field (case insensitive).
        :param query: string to search in database
        :return: query to use in django query methods (e.g. get, filter...)
        """
        return models.Q(title__icontains=query) | models.Q(title_pt__icontains=query)

    def get_title(self):
        return load_translated_field(self, 'title')

    class Meta:
        abstract = True


class TranslatableContent(models.Model):
    content = models.TextField()
    content_pt = models.TextField()

    def get_content(self):
        return load_translated_field(self, 'content')

    class Meta:
        abstract = True


class SocialNetwork(models.Model):
    AVAILABLE_SOCIALS = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'Linked In'),
        ('twitter', 'Twitter')
    )

    name = models.CharField(max_length=100, choices=AVAILABLE_SOCIALS)
    url = models.CharField(max_length=400)
    is_from_branch = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Social Networks"

    def render_icon(self):
        if self.name in [item[0] for item in self.AVAILABLE_SOCIALS]:  # preventing XSS's. Go away Manel.
            if self.is_from_branch:
                return '<span class="fa fa-%s"></span>' % self.name
            return '<a href="%s" class="fa fa-%s-square"></a>' % (self.url, self.name)
        return ''

    def __unicode__(self):
        return "%s with url %s" % (self.name, self.url)


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    ieee_contact = models.EmailField(unique=True, null=True)
    socials = models.ManyToManyField(SocialNetwork, blank=True)
    image = models.ImageField(upload_to=path_volunteers)

    def __unicode__(self):
        return self.name


class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    chair = models.ManyToManyField(Volunteer, blank=True, related_name="chair")
    vice_chair = models.ManyToManyField(Volunteer, related_name="vice_chair", blank=True)
    info = models.TextField()
    info_pt = models.TextField()
    image = models.ImageField(upload_to=path_communities, blank=True)
    newsletter_subscribe_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Communities"

    def get_short_name(self):
        result = ""
        for char in self.name:
            if char.isupper():
                result += char

        if self.name.startswith("Women"):
            return "WiE"

        return result

    def get_url(self):
        return self.get_short_name().lower() + "/"

    def get_short_lower_name(self):
        return self.get_short_name().lower()

    def get_tagname(self):
        return "#" + self.get_short_name()

    def get_news(self):
        return News.objects.filter(tags__name=self.get_tagname()).order_by("-date")

    def get_news_latest(self):
        return News.objects.filter(tags__name=self.get_tagname()).order_by("-date")[:5]

    def get_html_info(self):
        return markdown.markdown(load_translated_field(self, 'info'), output_format='html5')

    def get_newsletters(self):
        return self.newsletter_set.all().order_by('-created')

    def get_most_recent_newsletter(self):
        return self.newsletter_set.all().order_by('-created')[0]

    def get_photo_album(self):
        return settings.PHOTO_ALBUM_LOADER_INSTANCE.get_photos_url(self.get_short_lower_name())

    def get_initiatives(self):
        return list(Initiative.objects.filter(community__name=self.name))

    def __unicode__(self):
        return self.name


class Projects(models.Model):
    coordinator = models.ManyToManyField(Volunteer, blank=True)
    name = models.CharField(max_length=100)
    info = models.TextField()
    info_pt = models.TextField()
    image = models.ImageField(upload_to=path_projects, blank=True)

    class Meta:
        verbose_name_plural = "Projects"

    def get_short_name(self):
        result = ""
        for char in self.name:
            if char.isupper():
                result += char
        return result

    def get_short_lower_name(self):
        return self.get_short_name().lower()

    def get_url(self):
        return self.get_short_name().lower() + "/"

    def get_tagname(self):
        return "#" + self.get_short_name()

    def get_news(self):
        return News.objects.all().filter(tags__name=self.get_tagname()).order_by("-date")

    def get_news_latest(self):
        return self.get_news()[:5]

    def get_html_info(self):
        return markdown.markdown(load_translated_field(self, 'info'), output_format='html5')

    def __unicode__(self):
        return self.name


class Team(models.Model):
    begin_year = models.IntegerField()
    end_year = models.IntegerField()

    def __unicode__(self):
        return str(self.begin_year) + "/" + str(self.end_year)


class TeamMember(models.Model):
    role = models.CharField(max_length=50)
    member = models.ForeignKey(Volunteer)
    team = models.ForeignKey(Team)

    class Meta:
        verbose_name_plural = "Team Members"

    def __unicode__(self):
        return "%s - %s with role %s" % (self.team.__unicode__(), self.member.name, self.role)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    def get_nohashtag(self):
        return self.name[1:]


class News(TranslatableTitle, TranslatableContent):
    date = models.DateTimeField(auto_now_add=False)
    image = models.ImageField(upload_to=path_news, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    class Meta:
        verbose_name_plural = "News"

    def __unicode__(self):
        return "[%s] - %s" % (str(self.date), self.title)

    def get_html_content(self):
        return markdown.markdown(load_translated_field(self, 'content'), output_format='html5')

    def get_title(self):
        return load_translated_field(self, 'title')


class Partner(models.Model):
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to=path_initiatives)

    def __unicode__(self):
        return self.name


class Initiative(TranslatableUniqueTitle, TranslatableContent):
    community = models.ForeignKey(Community)
    partners = models.ManyToManyField(Partner, blank=True, null=True)
    image = models.ImageField(upload_to=path_initiatives, blank=True, null=True)

    def get_short_lower_name(self):
        r = ""
        for c in self.title.lower():
            if c.isalpha():
                r += c
        return r

    def get_ckeditor_content(self):
        return load_translated_field(self, 'content')

    def get_html_info(self):
        return markdown.markdown(load_translated_field(self, 'content'), output_format='html5')


class InitiativeEvent(TranslatableContent, TranslatableTitle):
    image = models.ImageField(upload_to=path_partners)
    date = models.DateTimeField()
    initiative = models.ForeignKey(Initiative)
    facebook = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.initiative.__unicode__()

    def get_html_info(self):
        return markdown.markdown(load_translated_field(self, 'content'), output_format='html5')


class Newsletter(TranslatableTitle):
    created = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(blank=False, null=False)
    pdf = models.FileField(upload_to=path_newsletters, validators=[validate_if_is_pdf_file],
                           blank=False, null=False)
    community = models.ForeignKey(Community, blank=False, null=False)

    def __unicode__(self):
        return self.get_title()

    def get_edition(self):
        ns = Newsletter.objects.filter(community=self.community).order_by('created')

        for i in range(ns.count()):
            if ns[i].id == self.id:
                return i + 1

        return -1
