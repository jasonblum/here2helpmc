import os, csv
from django.core.management.base import BaseCommand, CommandError

from orders.models import School



class Command(BaseCommand):
	help = 'Imports schools from https://data.montgomeryschoolsmd.org/browse?category=Schools'

	def handle(self, *args, **options):


		for school_type, filename in [
			('elementary', 'FY2014_General_Information_-_Elementary_Schools__2013-2014_.csv'),
			('middle', 'FY2014_General_Information_-_Middle_Schools__2013-2014_.csv'),
			('high', 'FY2014_General_Information_-_High_Schools__2013-2014_.csv'),
			]:
			
			filename = f'{os.getcwd()}/shared/management/commands/schools/{filename}'

			print(f'Importing {filename}...')

			f = open(filename)
			csv_reader = csv.reader(f)
			next(csv_reader)

			for row in csv_reader:
				print(row)

				school, _ = School.objects.update_or_create(
					mcps_school_id = int(row[1]),
					defaults = {
						'name' : row[2],
						'address' : row[3],
						'raw_address' : row[3], #address field is validated by Google API
						'phone' : row[6],
						'school_type' : school_type
					}
				)

				print(school.__dict__)


		self.stdout.write(self.style.SUCCESS('ok all done!'))
