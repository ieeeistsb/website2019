"""IEEESite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from app.models import Community, Projects
from app.views import *
from django.conf.urls import include, url
from django.db import ConnectionHandler
from django.db.migrations.recorder import MigrationRecorder
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from app.admin import admin_site


urlpatterns = i18n_patterns(
    url(r'^admin/', include(admin_site.urls)),
    url(r'^$', landing_page, name="landing"),
    url(r'^board/$', board, name="board"),
    url(r'^board/previous/$', previous_boards, name="previous_boards"),
    url(r'^contacts/$', contacts_view, name="contacts"),
    url(r'^about/ieee/$', about_ieee_view, name="about_ieee"),
    url(r'^news/all/$', all_news_view, name="all_news"),
    url(r'^news/(?P<news_id>[0-9]+)/$', specific_news_view, name="specific_news"),
    url(r'^communities/(?P<name>\w+)/$', page_view(Community), name="community"),
    url(r'^projects/(?P<name>\w+)/$', page_view(Projects), name="project"),
    url(r'^search/*', search, name="search"),
    url(r'^initiative/(?P<title>\w+)', initiative_view, name="initiative"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
