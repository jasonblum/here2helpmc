from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views import home, trigger_error



urlpatterns = [

    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('impersonate/', include('impersonate.urls')),

    path('accounts/', include('allauth.urls')),

	path('rosetta/', include('rosetta.urls')),
	path('i18n/', include('django.conf.urls.i18n')),
    path('djrichtextfield/', include('djrichtextfield.urls')),

	path('', home, name='home'),
    path('orders/', include('orders.urls')),

    path('map/', RedirectView.as_view(url=settings.GOOGLE_MAP_OF_DROPOFF_LOCATIONS), name='map'),


]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),

	path('error/', trigger_error),

    ]


handler400 = 'shared.views.handler400'
handler403 = 'shared.views.handler403'
handler404 = 'shared.views.handler404'
handler500 = 'shared.views.handler500'

admin.site.site_header = f'{settings.SITE_NAME}'
admin.site.site_title = f'{settings.SITE_NAME}'
admin.site.index_title = f'{settings.SITE_NAME} Administration Page'



