import pendulum, os
from csv import DictReader

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from stronghold.decorators import public

from address.models import Address, Locality

from shared.utilities import get_object_or_None

from .models import Order, Customer, School, Supporter, DropoffLocation, DeliveryDay
from .forms import StartForm, CustomerForm



def get_available_dates(customer):
	this_sunday = pendulum.now().start_of('week').subtract(days=1) #Weeks are Sunday-Saturday

	potential_dates = DeliveryDay.objects.filter(_date__gt=this_sunday)[:5]
	print('potential_dates: ', potential_dates)


	this_wednesday = this_sunday.next(pendulum.WEDNESDAY)
	next_sunday = this_sunday.add(weeks=1)
	next_wednesday = this_wednesday.add(weeks=1)
	
	DATES = []

	if not customer or not customer.this_weeks_orders:
		WEEK = [] 
		WEEK.append(_('This Week:'))
		#If now() is before noon the day before this Wednesday:
		if this_sunday.subtract(days=1).set(hour=12).is_future():
			WEEK.append(this_sunday)
		if this_wednesday.subtract(days=1).set(hour=12).is_future():
			WEEK.append(this_wednesday)
		DATES.append(WEEK)

	if not customer or not customer.next_weeks_orders:
		WEEK = [] 
		WEEK.append(_('Next Week:'))
		if next_sunday.subtract(days=1).set(hour=12).is_future():
			WEEK.append(next_sunday)
		if next_wednesday.subtract(days=1).set(hour=12).is_future():
			WEEK.append(next_wednesday)
		DATES.append(WEEK)

	print(DATES)

	return DATES






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

	if customer and not get_available_dates(customer):
		return redirect('orders:customer_event', customer_id=customer.pk, event='orders-already-filled')

	# Manually set language to customer.preferred_language? (https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#explicitly-setting-the-active-language)
	if request.POST and customer_form.is_valid():
		customer = customer_form.save()
		order = Order.objects.create(customer=customer, dt_requested_delivery = pendulum.parse(request.POST['dt_requested_delivery'], tz=settings.TIME_ZONE))
		return redirect('orders:customer_event', customer_id=customer.pk, event='order-just-placed')

	return render(request, 'orders/order.html', {'form':customer_form, 'available_dates': get_available_dates(customer)})	


@public
def customer(request, customer_id=None, event=''):
	customer = get_object_or_404(Customer, pk=customer_id)
	return render(request, 'orders/customer.html', {'customer':customer, 'event':event})	


def get_stats():
	stats = {
		'orders_created': Order.objects.filter(status='created').count(),
		'orders_ready': Order.objects.filter(status='ready').count(),
		'orders_delivered': Order.objects.filter(status='delivered').count(),
		'total_pounds_delivered': Order.objects.filter(status='delivered').count() * settings.ORDER_WEIGHT,
		'customers': Customer.objects.count(),
		'school_communities_served': School.objects.filter(customers__isnull=False).count(),
		'zipcodes_served': Locality.objects.count(),	
		#'start_date': Order.objects.filter(status='delivered').order_by('-dt_delivered').first().dt_delivered if Order.objects.exists() else None
		'start_date': None
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