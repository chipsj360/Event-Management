from django.contrib import admin
from .models import Venue,Event,Food, EventFood,EventAdmin
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Venue)
admin.site.register(Food)
admin.site.register(EventFood)
admin.site.register(Event, EventAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)