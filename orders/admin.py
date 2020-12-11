import pendulum
from django.contrib import admin, messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import TextInput, Textarea, EmailInput
from django.db import models
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from address.models import AddressField
from address.forms import AddressWidget

from import_export import resources
from import_export.admin import ExportActionMixin

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


def list_addresses(modeladmin, request, queryset):
	selected_order_ids = [o.id for o in queryset]
	orders = Order.objects.filter(pk__in=selected_order_ids)
	return render(request, 'orders/list_addresses.html', {
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

	if not orders.order_by().values('deliveryday').distinct().count() == 1:
		messages.error(request, f'You selected orders with different Delivery Days.')
		return redirect('admin:orders_order_changelist')

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
		

class DeliveryDayFilter(admin.SimpleListFilter):
	title = 'Delivery Day'
	parameter_name = 'deliveryday__id__exact'

	def lookups(self, request, model_admin):
		this_week_start = pendulum.now().start_of('week').subtract(days=1).subtract(weeks=1)

		deliverydays = DeliveryDay.objects.filter(_date__gte=this_week_start).order_by('_date')[:10]

		days = []
		for deliveryday in deliverydays:
			days.append( (deliveryday.pk, deliveryday) )
		return days

	def queryset(self, request, queryset):
		if self.value():
			return queryset.distinct().filter(deliveryday=self.value())
		else:
			return queryset
		
		

class BaseModelAdmin(ExportActionMixin, admin.ModelAdmin):
	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':'80'})},
		AddressField: {'widget': AddressWidget(attrs={'size':'80'})},
		models.EmailField: {'widget': EmailInput(attrs={'size':'80'})}
	}
	class Media:
		js = (
			'https://cdn.jsdelivr.net/npm/select2@4.1.0-beta.1/dist/js/select2.min.js',
			'shared/jQuery-Mask-Plugin-master/dist/jquery.mask.min.js', 
			'shared/admin.js', 
		)
		css = {'all': ('https://cdn.jsdelivr.net/npm/select2@4.1.0-beta.1/dist/css/select2.min.css', )}

	class Meta:
		abstract = True


		
@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
	search_fields = [
		'notes', 
		'customer__address__raw', 
		'customer__email', 
		'customer__passphrase', 
		'customer__comments', 
		'customer__notes', 
	]
	list_display = ('status', 'deliveryday', 'requires_admin_attention_flag', 'customer_link', 'customer_zip', 'driver', 'dt_created', 'dt_ready', 'dt_delivered', 'dt_cancelled', 'quick_note', )
	list_editable = ('quick_note', )
	list_filter = (DeliveryDayFilter, 'status', DriverFilter, 'customer_zip', )
	readonly_fields = ('status', 'customer_details')
	actions = (list_addresses, assign_these_orders_to_a_driver, get_email_to_send_driver, set_status_to_created, do_something_with_these_orders, do_something_else_with_these_orders, *ExportActionMixin.actions, )

	def has_add_permission(self, request, obj=None):
		return False

	def requires_admin_attention_flag(self, obj):
		return mark_safe('<img src="{}" alt="Requires Admin attention...">'.format(staticfiles_storage.url('/admin/img/icon-alert.svg'))) if obj.requires_admin_attention else ''
	requires_admin_attention_flag.short_description='Attention!'

	def customer_link(self, obj):
		return mark_safe('<a href="{}">{}</a>'.format(reverse('admin:orders_customer_change', args=[obj.pk]), obj.customer))
	requires_admin_attention_flag.short_description='Attention!'


@admin.register(Customer)
class CustomerAdmin(BaseModelAdmin):
	search_fields = ['email', 'address__raw', ]
	list_display = ('passphrase', 'address', 'email', 'phone', 'orders_created', 'orders_delivered', 'dt_created', )
	list_filter = ('address__locality', )

	def has_add_permission(self, request, obj=None):
		return False
		

@admin.register(Supporter)
class SupporterAdmin(BaseModelAdmin):
	list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'closest_dropoff_location', 'is_driver', 'orders_if_driver')
	search_fields = ['first_name', 'last_name', 'email', 'phone', 'address__raw', 'notes', ]
	list_filter = ('is_driver', )
	list_select_related = ('closest_dropoff_location', )

	def orders_if_driver(self, obj):
		order_count = obj.orders.count()
		if order_count:
			url = reverse('admin:orders_order_changelist') + '?driver__id__exact=' + str(obj.id)
			return format_html('<a href="{}">{} Order(s)</a>', url, order_count)
		else:
			return ''
	orders_if_driver.short_description = "Orders (if Driver)"


@admin.register(DropoffLocation)
class DropoffLocationAdmin(BaseModelAdmin):
	list_display = ('__str__', 'number_of_supporters')


@admin.register(School)
class SchoolAdmin(BaseModelAdmin):
	list_display = ('mcps_school_id', 'name', 'school_type', 'address', 'raw_address', 'phone', )


@admin.register(Donation)
class DonationAdmin(BaseModelAdmin):
	search_fields = ('supporter', )
	list_filter = ('method', )
	list_display = ('__str__', 'dt_created', 'date_received', 'date_thanked', 'thanked_by', 'ok_to_publicly_recognize', )	


@admin.register(DeliveryDay)
class DeliveryDayAdmin(BaseModelAdmin):
	list_display = ('__str__', 'description', 'number_of_orders', 'day_of_week_as_string', 'week_of_year', 'is_future', )
	
	def is_future(self, obj):
		return obj.date.is_future()
	is_future.boolean=True




# # https://django-import-export.readthedocs.io/ stuff

# class OrderResource(resources.ModelResource):
#     class Meta:
#         model = Order

# class SupporterResource(resources.ModelResource):
#     class Meta:
#         model = Supporter

