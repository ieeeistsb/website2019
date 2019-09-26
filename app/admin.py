from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

from app.models import *
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import User, Group


class IEEISTAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('IEEE-IST Student Branch Administration')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('IEEE-IST Student Branch Administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('IEEE-IST Student Branch Administration')


class ContentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    content_pt = forms.CharField(widget=CKEditorWidget())

    class Meta:
        abstract = True


admin_site = IEEISTAdminSite()
admin_site.register(SocialNetwork)
admin_site.register(Volunteer)
admin_site.register(Community)
admin_site.register(Projects)
admin_site.register(Team)

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role',)

admin_site.register(TeamMember, TeamMemberAdmin)

admin_site.register(News)
admin_site.register(Tag)


class InitiativeForm(ContentForm):
    class Meta:
        model = Initiative
        exclude = "__all__"


class InitiativeAdmin(admin.ModelAdmin):
    form = InitiativeForm


admin_site.register(Initiative, InitiativeAdmin)

admin_site.register(InitiativeEvent)
admin_site.register(Partner)
admin_site.register(Newsletter)
admin_site.register(User)
admin_site.register(Group)
