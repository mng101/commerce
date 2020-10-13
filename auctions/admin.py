from django.contrib import admin

# Register your models here.

from .models import Listing, Bid

admin.site.register(Listing)
admin.site.register(Bid)
