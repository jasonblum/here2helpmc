from django.urls import path


from .views import start, order, customer


app_name = 'orders'

urlpatterns = [

	path('', start, name='start'),
	path('order/<uuid:customer_id>/', order, name='order'),
	path('order/', order, name='order'),

	path('customer/<uuid:customer_id>/<slug:event>/', customer, name='customer_event'),
	path('customer/<uuid:customer_id>/', customer, name='customer'),

]