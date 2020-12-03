from django.contrib import admin

from .models import ExtraDelivery, CancelledDelivery


@admin.register(ExtraDelivery)
class ExtraDeliveryAdmin(admin.ModelAdmin):
	list_display = ('date', 'text', 'notes', )	

@admin.register(CancelledDelivery)
class CancelledDeliveryAdmin(admin.ModelAdmin):
	list_display = ('date', 'text', 'notes', )	
