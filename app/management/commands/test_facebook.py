from django.conf import settings
from django.core.management import BaseCommand
from app.fb.utils import get_page_incoming_events


class Command(BaseCommand):
    def handle(self, *args, **options):
        print get_page_incoming_events()

