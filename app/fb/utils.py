from django.conf import settings
import facebook
from datetime import datetime


def get_page_incoming_events():
    f = facebook.GraphAPI(version='2.7')
    f.access_token = f.get_app_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)

    events = f.get_object(settings.EVENTS_PAGE_ID + "/events?fields=cover,description,start_time,name")

    if not events:
        return list()

    events = events.get('data', None)
    if not events:
        return list()

    for event in events:
        cover = event.get('cover', None)

        if cover:
            event['cover'] = event['cover']['source']
        event['date'] = datetime.strptime(event.pop("start_time").split("+")[0], "%Y-%m-%dT%H:%M:%S")

    events.sort(key=lambda x: x['date'])
    events = [event for event in events if event['date'] > datetime.now()]

    return events[:5]

