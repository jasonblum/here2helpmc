import os, csv
from django.core.management.base import BaseCommand, CommandError

from address.models import Address

from orders.models import DropoffLocation, Supporter, Inventory



class Command(BaseCommand):
	help = 'Create dropoff locations'

	def handle(self, *args, **options):

		address = {
				'raw': 'Bethesda Presbyterian Church, 7611 Clarendon Road, Bethesda, MD  20814',
				'street_number': '7611',
				'route': 'Clarendon Road',
				'locality': 'Bethesda',
			    'postal_code': '20814',
				'state': 'Maryland',
				'state_code': 'MD',
				'country': 'United States',
				'country_code': 'US' 
		}

		supporter = Supporter.objects.create(
			first_name = 'Charles',
			last_name = 'Booker',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'Central Bethesda',
			address = address,
			url = 'https://www.signupgenius.com/go/20f094bafaa23a2fb6-bethesda',
			lead_supporter = supporter
		)

		address['raw'] = '3404 Thornapple Street  Chevy Chase, MD 20815'
		address['street_number'] = '3404'
		address['route'] = 'Thornapple Street'
		address['locality'] = 'Chevy Chase'
		address['postal_code'] = '20815'
		supporter = Supporter.objects.create(
			first_name = 'Barbara',
			last_name = 'Sacks',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'Chevy Chase',
			address = address,
			lead_supporter = supporter
		)

		address['raw'] = '4609 Windsor Ln Bethesda, MD 20814'
		address['street_number'] = '4609'
		address['route'] = 'Windsor Lane'
		address['locality'] = 'Bethesda'
		address['postal_code'] = '20814'
		supporter = Supporter.objects.create(
			first_name = 'Wendy',
			last_name = 'Vincente',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'East Bethesda',
			address = address,
			url = 'https://www.signupgenius.com/go/8050445a5a92e5-here2help',
			lead_supporter = supporter
		)

		address['raw'] = '3621 Littledale Rd Kensington, MD 20895'
		address['street_number'] = '3621'
		address['route'] = 'Littledale Road'
		address['locality'] = 'Kensington'
		address['postal_code'] = '20895'
		supporter = Supporter.objects.create(
			first_name = 'Paul',
			last_name = 'Beatty',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'Kensington',
			address = address,
			url = 'https://www.signupgenius.com/go/20f0a49a9af23a31-here',
			lead_supporter = supporter
		)

		address['raw'] = '3200 Farmington Dr Chevy Chase, MD 20815'
		address['street_number'] = '3200'
		address['route'] = 'Farmington Drive'
		address['locality'] = 'Chevy Chase'
		address['postal_code'] = '20815'
		supporter = Supporter.objects.create(
			first_name = 'Patricia',
			last_name = 'McDermott',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'North Chevy Chase',
			address = address,
			url = 'https://www.signupgenius.com/go/20f0d4faea929a6fe3-chevy',
			lead_supporter = supporter
		)

		address['raw'] = '8803 Maywood Ave Silver Spring, MD 20910'
		address['street_number'] = '8803'
		address['route'] = 'Maywood Avenue'
		address['locality'] = 'Silver Spring'
		address['postal_code'] = '20910'
		supporter = Supporter.objects.create(
			first_name = 'Kristin',
			last_name = 'Kramer',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'Rosemary Hills',
			address = address,
			url = 'https://www.signupgenius.com/go/409094daca92f4-rosemary',
			lead_supporter = supporter
		)

		address['raw'] = '4814 Falstone Ave Chevy Chase, MD 20815'
		address['street_number'] = '4814'
		address['route'] = 'Falstone Avenue'
		address['locality'] = 'Chevy Chase'
		address['postal_code'] = '20815'
		supporter = Supporter.objects.create(
			first_name = 'Hedy',
			last_name = 'Esfahanian',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'Somerset',
			address = address,
			url = 'https://www.signupgenius.com/go/20f0a4fa8aa2ea4fc1-neighborhood',
			lead_supporter = supporter
		)

		address['raw'] = '5123 Allan Terrace Bethesda, MD 20816'
		address['street_number'] = '5123'
		address['route'] = 'Allan Terrace'
		address['locality'] = 'Bethesda'
		address['postal_code'] = '20816'
		supporter = Supporter.objects.create(
			first_name = 'Cathy',
			last_name = 'Stocker',
			address = address
		)
		DropoffLocation.objects.create(
			inventory = Inventory.objects.create(),
			neighborhood = 'Westbrook',
			address = address,
			url = 'https://www.signupgenius.com/go/10c0545a4a92a1-grocery',
			lead_supporter = supporter
		)

		self.stdout.write(self.style.SUCCESS('ok all done!'))
