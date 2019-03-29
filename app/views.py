from app.fb.utils import get_page_incoming_events
from app.models import TeamMember, Team, News, Initiative, InitiativeEvent, Community
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, Http404
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.db.models import Q


def landing_page(request):
    facebook_events = get_page_incoming_events()
    return render(request, 'main.html', {'events': facebook_events, 'communities': Community.objects.all()})


@never_cache
def board(request):
    members = TeamMember.objects.select_related('member').prefetch_related('member__socials')\
        .filter(team=Team.objects.all().order_by("-end_year").first())
    return render(request, 'board.html', {'board': members})


def about_ieee_view(request):
    return render(request, "about_ieee.html")


def previous_boards(request):
    teams = Team.objects.all().order_by("-end_year")
    boards = TeamMember.objects.select_related('member').exclude(team=teams.first()).order_by("id")
    team = teams[1:]
    return render(request, 'past_boards.html', {'boards': boards, "teams": team})


def page_view(klazzz):

    @never_cache
    def view_func(request, name):
        for o in klazzz.objects.all():
            if o.get_short_lower_name() == name:
                return render(request, 'communities.html', {'object': o})
        raise Http404()

    return view_func


@never_cache
def contacts_view(request):
    return render(request, 'contacts.html')


def render_news(request, for_search=False):
    """
        Allows using the same template for displaying all news and search filtered news.
    """
    search_string = ""
    if not for_search:
        queryset = News.objects.all().order_by('-date')
    else:
        search_string = request.GET.get('q', "")
        if search_string == "":
            return all_news_view(request)

        queryset = News.objects.all()
        search_terms = search_string.split(" ")
        myfilter = Q(content__icontains=search_terms[0]) | Q(content_pt__icontains=search_terms[0]) | \
            Q(tags__name__contains=search_terms[0])

        if len(search_terms) > 1:
            for term in search_terms[1:]:
                myfilter = myfilter | Q(content__icontains=term) | Q(content_pt__icontains=term) | \
                           Q(tags__name__contains=term)

        queryset = queryset.filter(myfilter).distinct()

    paginator = Paginator(queryset, settings.OBJECTS_PER_PAGE, request=request)
    page = request.GET.get("page", 1)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'all_news.html', context={'all_news': news,
                                                     'for_search': for_search,
                                                     'search_string': search_string})


@never_cache
def all_news_view(request):
    return render_news(request, False)


def specific_news_view(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'specific_news.html', context={'news': news})


def search(request):
    return render_news(request, True)


def initiative_view(request, title):
    # Note that this query will return the same object regardless of user's language.
    # For example if your Initiative.title="foo" and Initiative.title_pt="bar" both of the following URLs will render
    # the exact same page: https://[...]/pt/initiative/foo/; https://[...]/pt/initiative/bar/
    initiative = None
    for i in Initiative.objects.all():
        if i.get_short_lower_name() == title.lower():
            initiative = i

    if initiative is None:
        raise Http404()

    return render(request, 'initiative.html', context={'object': initiative})


