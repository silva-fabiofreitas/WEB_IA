import csv
from django.core.management.base import BaseCommand
from core.models import Iris

class Command(BaseCommand):
    help = 'Importa dados de Iris do arquivo CSV'

    def handle(self, *args, **kwargs):
        with open('iris.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Iris.objects.create(
                    sepal_length=row['sepal.length'],
                    sepal_width=row['sepal.width'],
                    petal_length=row['petal.length'],
                    petal_width=row['petal.width'],
                    variety=row['variety']
                )
        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso'))
