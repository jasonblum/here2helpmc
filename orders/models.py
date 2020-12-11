from datetime import datetime
import pendulum
import uuid
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from annoying.fields import AutoOneToOneField
from djrichtextfield.models import RichTextField

from address.models import AddressField

from shared.utilities import get_object_or_None

class BaseModel(models.Model):
    dt_created = models.DateTimeField(verbose_name=_('Datetime created'), auto_now_add=True)
    dt_updated = models.DateTimeField(verbose_name=_('Datetime updated'), auto_now=True)

    def delete(self):
        raise PermissionDenied('This class of data cannot be deleted.')

    class Meta:
        abstract = True


class DeliveryDay(BaseModel):
    _date = models.DateField(unique=True)
    _week_of_year = models.PositiveSmallIntegerField(blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self._week_of_year = self.date.add(days=1).week_of_year if not self.date.day_of_week else self.date.week_of_year
        super(DeliveryDay, self).save(*args, **kwargs) 

    @property
    def date(self):
        return pendulum.parse(str(self._date), tz=settings.TIME_ZONE)

    @property
    def day_of_week(self):
        return self.date.day_of_week

    @property
    def week_of_year(self):
        return self._week_of_year

    @property
    def day_of_week_as_string(self):
        return self.date.format('dddd')

    @property
    def number_of_orders(self):
        return self.orders.count()

    def __str__(self):
        return str(self.date.format('dddd MMMM D, YYYY'))

    class Meta:
        ordering = ['_date', ]



SCHOOL_TYPE_CHOICES = (
    ('elementary', 'Elementary'),
    ('middle', 'Middle'),
    ('high', 'High'),
)

class School(BaseModel):
    mcps_school_id = models.PositiveSmallIntegerField(unique=True)
    school_type = models.CharField(max_length=10, choices=SCHOOL_TYPE_CHOICES)
    name = models.CharField(max_length=50)
    address = AddressField()
    raw_address = models.CharField(max_length=254, help_text='Raw address not yet validated by Google API.')
    phone = models.CharField(max_length=20, help_text='(301) 123-4567', validators=[MinLengthValidator(10)])

    class Meta:
        unique_together = ['name', 'school_type']

    def __str__(self):
        return self.name


class DropoffLocation(BaseModel):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    @property
    def number_of_supporters(self):
        return self.supporters.count()



class Supporter(BaseModel):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, help_text='(301) 123-4567', validators=[MinLengthValidator(10)], blank=True, null=True)
    address = AddressField(blank=True, null=True)
    closest_dropoff_location = models.ForeignKey(DropoffLocation, on_delete=models.PROTECT, related_name='supporters', blank=True, null=True)
    is_driver = models.BooleanField(default=False)
    notes = models.TextField(verbose_name=_('Notes'), blank=True, null=True)

    class Meta:
        unique_together = ['first_name', 'last_name', 'email', ]
        ordering = ['last_name', 'first_name', ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'




class Customer(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    passphrase = models.CharField(verbose_name=_('Passphrase'), max_length=20, help_text=_('Enter a name, word or phrase you can use next time to fill out most of this form for you.'))
    address = AddressField(verbose_name=_('Street Address'))
    phone = models.CharField(verbose_name=_('Phone'), max_length=20, help_text='This should preferably be a mobile phone number that can receive text messages.', validators=[MinLengthValidator(10)])
    phone_can_receive_texts = models.BooleanField(default=False, verbose_name=_('Texts?'), help_text=_('Can receive text messages?'))
    secondary_phone = models.CharField(verbose_name=_('Secondary Phone'), max_length=20, help_text='(301) 123-4567', blank=True, null=True, validators=[MinLengthValidator(10)])
    secondary_phone_can_receive_texts = models.BooleanField(default=False, verbose_name=_('Texts?'), help_text=_('Secondary Phone can receive text messages?'))
    email = models.EmailField(verbose_name=_('Email'), help_text='', blank=True, null=True)
    secondary_email = models.EmailField(verbose_name=_('Secondary Email'), help_text='', blank=True, null=True)
    apartment_number = models.CharField(verbose_name=_('Apartment Number'), max_length=10, blank=True, null=True)
    preferred_language = models.CharField(verbose_name=_('Preferred Language'), max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGES[0][0])
    household_size = models.PositiveSmallIntegerField(verbose_name=_('Household size'), default=2, choices=tuple(((i, i) for i in range(1, 11))), help_text=_('How many household members are you feeding?'))
    schools = models.ManyToManyField(School, verbose_name=_('MCPS Schools'), related_name='customers', blank=True, help_text=_('Continue clicking to add all schools that apply. (MCPS Schools only)'))
    special_requests = models.TextField(verbose_name=_('Special Requests'), null=True, blank=True, help_text=_('A limited amount of feminine hygiene and other non-food items are available upon request, on a first-come, first-served basis. Let us know if you need anything like this and please specify.'))
    dietary_restrictions = models.CharField(verbose_name=_('Dietary restrictions / Allergies'), max_length=254, null=True, blank=True, help_text=_('Vegetarian?  Gluten-free?  Is there anything you have no use for?'))
    comments = models.TextField(verbose_name=_('Comments'), null=True, blank=True, help_text=_('Delivery instructions or anything else we can help with?'))
    notes = models.TextField(verbose_name=_('Notes'), null=True, blank=True)

    def __str__(self):
        return f'Customer ("{self.passphrase}") at {self.address.street_number} {self.address.route} {self.address.locality.postal_code}'

    class Meta:
        ordering = ['-dt_created']
        unique_together = ['passphrase', 'address', ]

    @property
    def orders_delivered(self):
        return self.orders.filter(status='delivered').count()

    @property
    def orders_created(self):
        return self.orders.filter(status='created').count()

    @property
    def this_weeks_orders(self):
        #Customer is only allowed on order a week.
        return self.orders.filter(
            dt_requested_delivery__range=(
                    pendulum.now().start_of('week').subtract(days=1), 
                    pendulum.now().end_of('week').subtract(days=1)
                )
            )

    @property
    def next_weeks_orders(self):
        #Customer is only allowed on order a week.
        return self.orders.filter(
            dt_requested_delivery__range=(
                    pendulum.now().start_of('week').add(weeks=1).subtract(days=1), 
                    pendulum.now().end_of('week').add(weeks=1).subtract(days=1)
                )
            )


class Order(BaseModel):
    status = models.CharField(max_length=9, choices=settings.ORDER_STATUS_CHOICES, default=settings.ORDER_STATUS_CHOICES[0][0])
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    customer_zip = models.CharField(max_length=5)
    deliver_to_address = AddressField(blank=True, null=True, verbose_name=_('Street Address Delivered'))
    driver = models.ForeignKey(Supporter, blank=True, null=True, on_delete=models.PROTECT, related_name='orders', limit_choices_to={'is_driver': True})

    dt_ready = models.DateTimeField(verbose_name=_('Datetime ready'), blank=True, null=True)
    deliveryday = models.ForeignKey(DeliveryDay, on_delete=models.PROTECT, related_name='orders')
    dt_delivered = models.DateTimeField(verbose_name=_('Datetime delivered'), blank=True, null=True)
    dt_cancelled = models.DateTimeField(verbose_name=_('Datetime cancelled'), blank=True, null=True)

    notes = models.TextField(verbose_name=_('Notes'), default='Notes:')
    requires_admin_attention = models.BooleanField(default=False)

    quick_note = models.CharField(verbose_name=_('Quick Note'), blank=True, null=True, max_length=255)
    __original_quick_note = None

    def __init__(self, *args, **kwargs):
        #https://stackoverflow.com/a/1793323
        super(Order, self).__init__(*args, **kwargs)
        self.__original_quick_note = self.quick_note

    def save(self, *args, **kwargs): 

        if self.quick_note and self.quick_note != self.__original_quick_note:
            self.notes += f'\nQuick note ({pendulum.now()}): ' + self.quick_note

        if self.driver and not self.driver.is_driver:
            #I think this is covered by limit_choices_to, but just in case.
            raise Exception('Driver must have is_driver set to True')

        if self.dt_cancelled:
            self.status = 'cancelled'
        elif self.dt_delivered:
            self.status = 'delivered'
        elif self.dt_ready:
            self.status = 'ready'
        elif self.driver:
            self.status = 'processed'
        else:
            self.status='created'
            self.deliver_to_address = self.customer.address #In case the customer changes their address later?
            self.customer_zip = self.customer.address.as_dict()['postal_code'][:5]

        super(Order, self).save(*args, **kwargs) 

    def get_absolute_url(self):
        return reverse(f'{self._meta.app_label}:detail', args=[self.pk])

    def __str__(self):
        return f'Order #{self.pk} for {self.customer} (status: {self.status})'

    @property
    def zip(self):
        return self.customer.address.as_dict()['postal_code']

    @property
    def customer_details(self):
        return mark_safe(f'''<li>Address: {self.customer.address}</li>
<li>Phone: {self.customer.phone} (Can receive texts? {self.customer.phone_can_receive_texts})</li>
<li>Secondary Phone: {self.customer.phone} (Can receive texts? {self.customer.secondary_phone_can_receive_texts})</li>
<li>Email: {self.customer.email}</li>
<li>Secondary Email: {self.customer.secondary_email}</li>
<li>Apartment: {self.customer.apartment_number}</li>
<li>Preferred Language: {self.customer.get_preferred_language_display()}</li>
<li>Special Requests: {self.customer.special_requests}</li>
<li>Dietary Restrictions: {self.customer.dietary_restrictions}</li>
<li>Comments: {self.customer.comments}</li>''')

    class Meta:
        ordering = ['-dt_created']




DONATION_METHOD_CHOICES = (
    ('cash', 'Cash'),
    ('check', 'Check'),
    ('credit', 'Credit'),
    ('paypal', 'PayPal'),
    ('venmo', 'Venmo'),
)



class Donation(BaseModel):
    supporter = models.ForeignKey(Supporter, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    method = models.CharField(max_length=6, choices=DONATION_METHOD_CHOICES)
    payment_details = models.CharField(max_length=254, null=True, blank=True, help_text='Check #, Credit Card type, etc.')
    date_received = models.DateField(verbose_name=_('Date donation received'), blank=True, null=True)
    ok_to_publicly_recognize = models.BooleanField(default=False)
    preferred_wording_for_public_recognition = models.TextField(null=True, blank=True)
    other_donor_specifications = models.TextField(null=True, blank=True)
    date_thanked = models.DateField(verbose_name=_('Date thanked'), blank=True, null=True, help_text='Who sent the thank-you and how?')
    thanked_by = models.CharField(max_length=254, null=True, blank=True, help_text='Who sent the thank-you and how?')
    notes = models.TextField(null=True, blank=True, help_text='Any additional notes on this donation?')

    def __str__(self):
        return f'Donation of {self.amount} from {self.supporter}'

    class Meta:
        ordering = ['-amount']
