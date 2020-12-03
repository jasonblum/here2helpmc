from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions

from address.forms import AddressWidget, AddressField

from .models import Customer

#Doing this: https://studygyaan.com/django/how-to-use-bootstrap-4-forms-with-django-crispy-forms



class StartForm(forms.Form):
	passphrase = forms.CharField(
		label='passphrase',
		max_length=20,
		required=True
	)
	address = AddressField()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['address'].widget = AddressWidget()
		self.helper.layout = Layout(
			'passphrase',
			'address',
			Div(
				FormActions(Submit('create', 'Make a request!', css_class='btn-primary btn-lg m-3')),
				css_class='text-center'
			)
		)



class CustomerForm(forms.ModelForm):

	class Meta:
		model = Customer
		fields = (
			'passphrase', 
			'address', 
			'apartment_number', 
			'preferred_language', 
			'phone',
			'phone_can_receive_texts',
			'secondary_phone',
			'secondary_phone_can_receive_texts',
			'email',
			'secondary_email',
			'household_size', 
			'schools', 
			'special_requests', 
			'dietary_restrictions', 
			'comments', 
		)

	dt_requested_delivery = forms.CharField(widget=forms.Select, label=_('Desired delivery day'), help_text=_('Please request only one delivery per week (Sunday-Saturday).'))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['address'].widget = AddressWidget()	

		self.helper.layout = Layout(


			Div(
				Div(
					Field(
						PrependedText('passphrase',
							mark_safe('<i class="fas fa-key"></i>'),
							placeholder=_("Name, word or phrase..."))
						),
						css_class='col-md-6'
				),
				Div(
					Field(
						PrependedText('address',
							mark_safe('<i class="fas fa-map-marker-alt"></i>'),
							placeholder=_("Enter your address in Montgomery County, MD"))
						),
						css_class='col-md-6'
				), css_class='row'
			),



			Div(
				Div(
					Field(
						PrependedText('dt_requested_delivery',
							mark_safe('<i class="fas fa-clock"></i>'),
							)
						),
						css_class='col-md-6'
				),
				css_class='row'
			),


			Div(
				Div(
					Field(
						PrependedText('preferred_language',
							mark_safe('<i class="fas fa-globe"></i>'),
							)
						),
						css_class='col-md-6'
				),
				Div(
					Field(
						PrependedText('apartment_number',
							mark_safe('<i class="fas fa-door-open"></i>'),
							placeholder=_("Do you have an apartment number?"))
						),
						css_class='col-md-6'
				), css_class='row'
			),



			Div(
				Div(
					Field(
						PrependedText('phone',
							mark_safe('<i class="fas fa-phone"></i>'),
							placeholder=_("(999) 999-9999"))
						),
						css_class='col-md-6'
				),
				Div(
					Field(
						PrependedText('secondary_phone',
							mark_safe('<i class="fas fa-phone"></i>'),
							placeholder=_("Enter Secondary Phone"))
						),
						css_class='col-md-6'
				), css_class='row'
			),

			Div(
				Div(
					Field(
						'phone_can_receive_texts'						
						),
						css_class='col-md-6'
				),
				Div(
					Field(
						'secondary_phone_can_receive_texts'						
						),
						css_class='col-md-6'
				),
				css_class='row'
			),



			Div(
				Div(
					Field(
						PrependedText('email',
							mark_safe('<i class="far fa-envelope"></i>'),
							placeholder=_("Enter Primary Email"))
						),
						css_class='col-md-6'
				),
				Div(
					Field(
						PrependedText('secondary_email',
							mark_safe('<i class="far fa-envelope"></i>'),
							placeholder=_("Enter Secondary Email"))
						),
						css_class='col-md-6'
				), css_class='row'
			),

			Div(
				Div(
					Field(
						PrependedText('household_size',
							mark_safe('<i class="fas fa-users"></i>'),
							placeholder=_("Household size"))
						),
						css_class='col-md-6'
				),
				Div(
					Field(
						PrependedText('schools',
							mark_safe('<i class="fas fa-school"></i>'),
							placeholder=_("Enter schools"))
						),
						css_class='col-md-6'
				), css_class='row'
			),

			Field(
				PrependedText('special_requests',
					mark_safe('<i class="far fa-comments"></i>'),
					placeholder=_("Any special requests?"))
				),
			Field(
				PrependedText('dietary_restrictions', mark_safe('<i class="fas fa-utensils"></i>'))
				),
			Field(
				PrependedText('comments',
					mark_safe('<i class="far fa-comments"></i>'),
					placeholder=_("Comments?"))
				),
			Div(
				FormActions(Submit('create', 'Make a request!', css_class='btn-primary btn-lg')),
				css_class='text-center'
			)
		)

	def clean_address(self):
		data = self.cleaned_data['address']
		zip = data.as_dict()['postal_code']
		if not zip in settings.MONTGOMERY_COUNTY_ZIPCODES:
			raise ValidationError('Please select an address having a zip code in Montgomery County, Maryland.')
		return data