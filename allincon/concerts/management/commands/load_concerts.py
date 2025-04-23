import json
from django.core.management.base import BaseCommand
from concerts.models import Concert, Site, Location

class Command(BaseCommand):
    help = "Load concerts, sites, and locations from JSON files"

    def handle(self, *args, **options):
        with open('data/site.json', 'r', encoding='utf-8') as f:
            sites = json.load(f)
        for item in sites:
            Site.objects.update_or_create(
                id=item['id'],
                defaults={'name': item['site']}
            )
        self.stdout.write(self.style.SUCCESS(f'{len(sites)} sites loaded.'))

        with open('data/locationId.json', 'r', encoding='utf-8') as f:
            locations = json.load(f)
        for item in locations:
            Location.objects.update_or_create(
                id=item['id'],
                defaults={'name': item['location']}
            )
        self.stdout.write(self.style.SUCCESS(f'{len(locations)} locations loaded.'))

        with open('data/concerts.json', 'r', encoding='utf-8') as f:
            concerts = json.load(f)
        for item in concerts:
            Concert.objects.update_or_create(
                title=item['title'],
                start_date=item['start_date'],  # 이 둘의 조합을 기준으로 찾는다
                defaults={
                    'end_date': item['end_date'],
                    'location_id': item['location'],
                    'site_id': item['site'],
                }
            )
        self.stdout.write(self.style.SUCCESS(f'{len(concerts)} concerts loaded.'))
