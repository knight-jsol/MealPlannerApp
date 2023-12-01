import csv
from django.core.management.base import BaseCommand
from webpage.models import Ingredients


class Command(BaseCommand):
    help = 'Import ingredients from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Ingredients.objects.create(
                    food=row['Food'],
                    measure=row['Measure'],
                    grams=row['Grams'],
                    calories=row['Calories'],
                    fat=row['Fat'],
                    sat_fat=row['Sat.Fat'],
                    fiber=row['Fiber'],
                    carbs=row['Carbs'],
                    category=row['Category']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported ingredients'))
