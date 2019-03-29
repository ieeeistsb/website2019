from app.models import Tag, News
from django.core.management import BaseCommand
from loremipsum import generate_paragraph
from loremipsum import generate_sentence
import random

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            news_content = ""
            for j in range(random.randint(1,4)):
                news_content = news_content + generate_paragraph()[2] + "\n"

            title = generate_sentence(start_with_lorem=True)[2]
            if len(title) > 50:
                title = title[0:50]

            news = {
                'content': news_content,
                'content_pt': news_content,
                'title': title,
                'title_pt': title
            }
            News.objects.create(**news)
            self.stdout.write("Created news number " + str(i))
