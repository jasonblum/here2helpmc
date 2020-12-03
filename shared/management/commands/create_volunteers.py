"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

User = get_user_model()


MODELS = ['Customer', 'DropoffLocation', 'Order', 'School', 'Supporter', 'User', 'Delivery', 'Inventory', 'Donation', ]
PERMISSIONS = ['add', 'change', 'view', ]


class Command(BaseCommand):
	help = 'Creates read only default permission groups for users'

	def handle(self, *args, **options):
		volunteers, created = Group.objects.get_or_create(name='volunteers')

		for model in MODELS:
			for permission in PERMISSIONS:
				codename = f'{permission}_{model.lower()}'

				model_add_perm = Permission.objects.get(codename=codename)
				
				volunteers.permissions.add(model_add_perm)
			
		print('Volunteers group created with permissions')

		u1 = User.objects.create_user(
			email='lbehbehani8@gmail.com',
			password='admin'
		)
		u2 = User.objects.create_user(
			email='sharonkangas@yahoo.com',
			password='admin'
		)
		u3 = User.objects.create_user(
			email='admin@admin.com',
			password='admin'
		)

		u1.is_staff=True
		u1.save()
		u2.is_staff=True
		u2.save()
		u3.is_staff=True
		u3.save()

		volunteers.user_set.add(u1)
		volunteers.user_set.add(u2)
		volunteers.user_set.add(u3)

		print('Lily and Sharon added to volunteers group')


		print("Created default group and permissions.")