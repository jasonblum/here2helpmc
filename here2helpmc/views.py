from stronghold.decorators import public
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext_lazy as _

from orders.views import get_stats

@public
def home(request):
	return render(request, 'home.html', {'stats':get_stats()})



@public
def trigger_error(request):
	division_by_zero = 1 / 0