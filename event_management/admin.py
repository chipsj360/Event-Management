from django.contrib import admin
from .models import Venue,Event,Food, EventFood,EventAdmin

# Register your models here.
admin.site.register(Venue)
admin.site.register(Food)
admin.site.register(EventFood)
admin.site.register(Event, EventAdmin)
