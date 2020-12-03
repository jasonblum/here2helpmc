import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone



User = get_user_model()


class Command(BaseCommand):
	help = 'Sets up initial data (schools, admin account, etc.)'

	def handle(self, *args, **options):

		os.remove(settings.DATABASES['default']['NAME'])
		print(f'Deleted: {settings.DATABASES["default"]["NAME"]}')

		call_command('migrate')
		print('New database created and migrated')

		User.objects.create_superuser(
			password='admin',
			email=settings.ADMIN_EMAIL,
		)
		print('admin created')

		call_command('import_schools')
		print('Schools imported')

		call_command('create_volunteers')
		print('volunteers created')

		call_command('create_dropoff_locations')
		print('dropoff_locations created')

		# call_command('loaddata', 'orders.json', stdout=out, verbosity=0)
		# print('orders.json data loaded')


		self.stdout.write(self.style.SUCCESS('ok all done!'))






