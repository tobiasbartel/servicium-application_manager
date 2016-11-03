from django.core.management.base import BaseCommand, CommandError
from servicecatalog.models import Module
from instance_manager.models import Instance, Location, PROD
import csv
from pprint import pprint

class Command(BaseCommand):
    help = 'Import a list of modules from CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for csv_filename in options['file_name']:
            with open(csv_filename, 'rb') as my_csv:
                reader = csv.reader(my_csv)
                for row in reader:
                    pprint(row[0])
                    module, module_created = Module.objects.get_or_create(name=row[1].strip().encode('UTF-8'))
                    module.description = row[0].strip()
                    pprint(module)
                    if module_created:
                        module.save()
                    else:
                        my_location = Location.objects.get(pk=1)
                        try:
                            instance, instance_created = Instance.objects.get_or_create(name=row[2], environment=PROD, module=module, location=my_location)
                        except:
                            instance_created = False
                        if instance_created:
                            instance.module=module
                            instance.environment=PROD
                            instance.name=row[2]