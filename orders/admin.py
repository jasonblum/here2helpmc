import pendulum
from django.contrib import admin, messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import TextInput, Textarea, EmailInput
from django.db import models
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe

from address.models import AddressField
from address.forms import AddressWidget

from .models import Order, Customer, School, Supporter, Donation, DropoffLocation, DeliveryDay


def do_something_with_these_orders(modeladmin, request, queryset):
	selected_order_ids = [o.id for o in queryset]
	orders = Order.objects.filter(pk__in=selected_order_ids)
	return render(request, 'orders/do_something_with_these_orders.html', {
		'orders':orders,
	})	


def do_something_else_with_these_orders(modeladmin, request, queryset):
	selected_order_ids = [o.id for o in queryset]
	orders = Order.objects.filter(pk__in=selected_order_ids)
	return render(request, 'orders/do_something_with_these_orders.html', {
		'orders':orders,
	})	


def set_status_to_created(modeladmin, request, queryset):
	selected_order_ids = [o.id for o in queryset]
	orders = Order.objects.filter(pk__in=selected_order_ids)
	for order in orders:
		order.dt_cancelled = None
		order.dt_delivered = None
		order.dt_ready = None
		order.driver = None
		order.save()
	messages.success(request, f'{len(orders)} orders\' statuses reset to created.')
	return redirect('admin:orders_order_changelist')


def assign_these_orders_to_a_driver(modeladmin, request, queryset):
	selected_order_ids = [o.id for o in queryset]
	drivers = Supporter.objects.filter(is_driver=True)
	orders = Order.objects.filter(pk__in=selected_order_ids, status='created')
	return render(request, 'orders/assign_orders_to_drivers.html', {
		'orders':orders,
		'drivers': drivers,
	})	

def get_email_to_send_driver(modeladmin, request, queryset):
	selected_order_ids = [o.id for o in queryset]
	orders = Order.objects.filter(pk__in=selected_order_ids, status='processed')

	if not orders:
		messages.error(request, f'You didn\'t select any orders with a status of \'processed\'.')
		return redirect('admin:orders_order_changelist')

	if orders.order_by().values('driver').distinct().count() != 1:
		messages.error(request, f'You selected orders with more than one driver.')
		return redirect('admin:orders_order_changelist')

	driver = orders[0].driver #they must all have the same driver at this point.

	email = render_to_string('emails/email_to_driver.html', {'driver': driver, 'orders':orders})

	return render(request, 'orders/email_to_driver.html', {'driver':driver, 'orders':orders, 'email':email})

		




class DTRequestedDeliveryFilter(admin.SimpleListFilter):
	title = 'Requested Delivery Date'
	parameter_name = 'dt_requested_delivery' # you can put anything here

	def lookups(self, request, model_admin):
		start = pendulum.now().subtract(weeks=1)
		end = pendulum.now().add(weeks=100)
		#dates = Order.objects.filter(dt_requested_delivery__range=(start, end)).values_list('dt_requested_delivery', flat=True)
		dates = []
		dates = list(set(dates))
		dates_to_return = []
		for date in dates:
			dates_to_return.append((date, date.strftime('%A %B %d, %Y')))
		return sorted(dates_to_return)

	def queryset(self, request, queryset):
		if self.value():
			return queryset.distinct().filter(dt_requested_delivery=self.value())
		else:
			return queryset
		
		
class DriverFilter(admin.SimpleListFilter):
	title = 'Driver'
	parameter_name = 'driver__id__exact'

	def lookups(self, request, model_admin):
		supporter_drivers = Supporter.objects.filter(is_driver=True, orders__isnull=False)
		drivers = []
		for sd in supporter_drivers:
			drivers.append( (sd.pk, sd) )
		return drivers

	def queryset(self, request, queryset):
		if self.value():
			return queryset.distinct().filter(driver=self.value())
		else:
			return queryset
		
		
		
		
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	search_fields = [
		'notes', 
		'customer__address__raw', 
		'customer__email', 
		'customer__passphrase', 
		'customer__comments', 
		'customer__notes', 
	]
	list_display = ('status', 'requires_admin_attention_flag', 'customer_link', 'customer_zip', 'dt_created', 'dt_ready', 'driver', 'deliveryday', 'dt_delivered', 'dt_cancelled', 'quick_note', )
	list_editable = ('quick_note', )
	list_filter = ('status', DriverFilter, 'customer_zip', DTRequestedDeliveryFilter, )
	readonly_fields = ('status', 'customer_details')
	actions = (assign_these_orders_to_a_driver, get_email_to_send_driver, set_status_to_created, do_something_with_these_orders, do_something_else_with_these_orders, )

	def has_add_permission(self, request, obj=None):
		return False

	def requires_admin_attention_flag(self, obj):
		return mark_safe('<img src="{}" alt="Requires Admin attention...">'.format(staticfiles_storage.url('/admin/img/icon-alert.svg'))) if obj.requires_admin_attention else ''
	requires_admin_attention_flag.short_description='Attention!'

	def customer_link(self, obj):
		return mark_safe('<a href="{}">{}</a>'.format(reverse('admin:orders_customer_change', args=[obj.pk]), obj.customer))
	requires_admin_attention_flag.short_description='Attention!'




@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	search_fields = ['email', 'address__raw', ]
	list_display = ('passphrase', 'address', 'email', 'phone', 'orders_created', 'orders_delivered', 'dt_created', )
	list_filter = ('address__locality', )
	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':'60'})},
		AddressField: {'widget': AddressWidget(attrs={'size':'80'})},
		models.EmailField: {'widget': EmailInput(attrs={'size':'60'})},
	}

	def has_add_permission(self, request, obj=None):
		return False


# class FilterByDriversZipCode(admin.SimpleListFilter):
# 	title = 'Driver\'s Zip Code (if driver)'
# 	parameter_name = 'zip' # you can put anything here

# 	def lookups(self, request, model_admin):
# 		zips = list((z, z) for z in Supporter.objects.filter(is_driver=True).values_list('address__locality__postal_code', flat=True).distinct())
# 		return zips

# 	def queryset(self, request, queryset):
# 		if self.value():
# 			return queryset.distinct().filter(is_driver=True, address__locality__postal_code=self.value())
# 		else:
# 			return queryset
		
		


@admin.register(Supporter)
class SupporterAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'closest_dropoff_location', 'is_driver', )
	search_fields = ['first_name', 'last_name', 'email', 'phone', 'address__raw', ]
	list_filter = ('is_driver', )


@admin.register(DropoffLocation)
class DropoffLocationAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'number_of_supporters')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ('mcps_school_id', 'name', 'school_type', 'address', 'raw_address', 'phone', )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
	search_fields = ('supporter', )
	list_filter = ('method', )
	list_display = ('__str__', 'dt_created', 'date_received', 'date_thanked', 'thanked_by', 'ok_to_publicly_recognize', )	


@admin.register(DeliveryDay)
class DeliveryDayAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'number_of_orders', 'day_of_week_as_string', 'week_of_year', 'is_future', )
	
	def is_future(self, obj):
		return obj.date.is_future()
	is_future.boolean=True

