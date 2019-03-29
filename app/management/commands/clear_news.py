from app.models import News
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        News.objects.all().delete()