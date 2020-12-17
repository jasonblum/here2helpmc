import pendulum, os
from collections import defaultdict
from csv import DictReader

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from stronghold.decorators import public

from address.models import Address, Locality

from shared.utilities import get_object_or_None

from .models import Order, Customer, School, Supporter, DropoffLocation, DeliveryDay
from .forms import StartForm, CustomerForm



def get_deliverydays(customer):
	this_week_start = pendulum.now().start_of('week').subtract(days=1) #Weeks are Sunday-Saturday

	potential_deliverydays = DeliveryDay.objects.filter(_date__gte=this_week_start, is_active=True).order_by('_date')[:10]

	deliverydays = defaultdict(list)
	
	for deliveryday in potential_deliverydays:

		if deliveryday.date.subtract(days=1).set(hour=12).is_future()\
			and not DeliveryDay.objects.filter(orders__customer=customer, orders__deliveryday___week_of_year=deliveryday.week_of_year).exists():

			deliverydays[deliveryday.week_of_year].append(deliveryday)

	return dict(deliverydays) #Django templates can't do defaultdict apparently?






@public
def start(request):
	start_form = StartForm(request.POST or None)
	if request.POST and start_form.is_valid():
		passphrase = start_form.cleaned_data['passphrase']
		address = start_form.cleaned_data['address']
		customer = get_object_or_None(Customer, passphrase=passphrase, address=address)
		if customer:
			return redirect('orders:order', customer_id=customer.pk)
		else:
			messages.warning(request, f'Are you sure youve ordered before?  I could not find a customer using the passphrase "{ passphrase }" at the address { address }.')
			return redirect('orders:start')
	return render(request, 'orders/start.html', {'form':start_form})	


@public
def order(request, customer_id=None):
	customer = get_object_or_None(Customer, pk=customer_id)
	customer_form = CustomerForm(request.POST or None, instance=customer)

	if customer and not get_deliverydays(customer):
		return redirect('orders:customer_event', customer_id=customer.pk, event='orders-already-filled')

	# Manually set language to customer.preferred_language? (https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#explicitly-setting-the-active-language)
	if request.POST and customer_form.is_valid():
		deliveryday = get_object_or_404(DeliveryDay, pk=request.POST['deliveryday'], is_active=True)
		customer = customer_form.save()
		order = Order.objects.create(customer=customer, deliveryday=deliveryday)

		if Customer.objects.filter(address=customer.address).count() > 1:
			requires_admin_attention_note = ''

			if (customer.email and Customer.objects.filter(Q(email=customer.email)|Q(secondary_email=customer.email)).count() > 1) or \
				(customer.secondary_email and Customer.objects.filter(Q(email=customer.secondary_email)|Q(secondary_email=customer.secondary_email)).count() > 1):
				requires_admin_attention_note += '\nRequires Admin Attention: More than one customer is using this address and email.  (What additional information could you use here?)'

			if (customer.phone and Customer.objects.filter(Q(phone=customer.phone)|Q(secondary_phone=customer.phone)).count() > 1) or \
				(customer.secondary_phone and Customer.objects.filter(Q(phone=customer.secondary_phone)|Q(secondary_phone=customer.secondary_phone)).count() > 1):
				requires_admin_attention_note += '\nRequires Admin Attention: More than one customer is using this address and phone.  (What additional information could you use here?)'

			if requires_admin_attention_note:
				order.notes += requires_admin_attention_note
				order.requires_admin_attention = True
				order.save()




		return redirect('orders:customer_event', customer_id=customer.pk, event='order-just-placed')

	print(customer_form.errors)

	return render(request, 'orders/order.html', {'form':customer_form, 'deliverydays': get_deliverydays(customer)})	


@public
def customer(request, customer_id=None, event=''):
	customer = get_object_or_404(Customer, pk=customer_id)
	return render(request, 'orders/customer.html', {'customer':customer, 'event':event})	


def get_stats():
	
	stats = {
		'orders_created': Order.objects.filter(status='created').count(),
		'orders_ready': Order.objects.filter(status='ready').count(),
		'orders_delivered': Order.objects.filter(status='delivered').count(),
		'total_pounds_delivered': Order.objects.filter(status='delivered').distinct().count() * settings.ORDER_WEIGHT,
		'customers': Customer.objects.count(),
		'school_communities_served': School.objects.filter(customers__isnull=False).distinct().count(),
		'zipcodes_served': Locality.objects.filter(addresses__customers__isnull=False).distinct().count(),	
		'start_date': Order.objects.order_by('-dt_created').first().dt_created
	}
	return stats



##admin functions
def assign_driver(request):
	order_pks = request.POST.getlist('orders')
	driver_pk = request.POST.get('driver', 0)

	driver = get_object_or_404(Supporter, pk=driver_pk)

	if not order_pks:
		messages.warning(request, f'Hm. You didn\t select any orders to assign to {driver}.  Try again?')
		return redirect('admin:orders_order_changelist')

	orders = []
	for pk in order_pks:
		order = Order.objects.get(pk=pk, status='created')
		order.driver = driver
		order.save()
		orders.append(order)

	messages.success(request, f'{len(orders)} orders assigned to {driver}')
	return redirect('admin:orders_order_changelist')







def import_supporters():
	raise
	with open(os.path.join(settings.BASE_DIR, 'docs/Here2Help Volunteers (Responses) - Form Responses 1.csv'), 'r') as data:
		reader = DictReader(data)

		for row in reader:

			first_name=row['first'].strip()
			last_name=row['last'].strip()
			email=row['email'].strip()
			raw_phone= ''.join([n for n in row['phone'].strip() if n.isdigit()]) 
			if raw_phone and raw_phone[0] == '1':
				raw_phone = raw_phone[1:]
			phone=f'({raw_phone[:3]}) {raw_phone[3:6]}-{raw_phone[6:]}'
			which=row['which'].strip()
			is_driver=row['willing'].strip()

			if which:
				dropoff_location, created = DropoffLocation.objects.get_or_create(name=which)

			supporter, created = Supporter.objects.get_or_create(
				first_name=first_name,
				last_name=last_name,
				email=email,
				is_driver= True if is_driver=='Yes' else False,
				phone=phone if raw_phone else None,
				closest_dropoff_location=dropoff_location if which else None
			)
			print(supporter)
	print('\n\n\nDONE!')