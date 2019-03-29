import datetime
from django.db import models
from django.utils.translation import ugettext_lazy  as _

# Create your models here.

YEAR_CHOICES = [(r, r) for r in range(2014, datetime.datetime.now().year + 1)]


class Competition(models.Model):
    year = models.IntegerField(verbose_name=_('Year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.CharField(max_length=1000, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Competition")
        verbose_name_plural = _("Competitions")

    def __str__(self):
        return "PyChallenge " + str(self.year)

    def get_games(self):
        return self.game_set.all().order_by("name")


class Game(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    url = models.CharField(max_length=250, verbose_name=_("Url"))
    authors = models.CharField(max_length=1000, verbose_name=_("Authors"))
    image = models.ImageField(upload_to="games_images", verbose_name=_("Image"))
    competition = models.ForeignKey(Competition, verbose_name=_("Competition"))

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")

    def __str__(self):
        return self.name


class Supporter(models.Model):
    logo = models.ImageField(upload_to="supporter", verbose_name=_("Logo"))
    website = models.CharField(max_length=250)

    class Meta:
        verbose_name = _("Supporter")
        verbose_name_plural = _("Supporters")
