from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import admin

class BaseModel(models.Model):
  created_at = models.DateTimeField(default=now, editable=False)
  created_by = models.IntegerField(null=True, blank=True)
  datemodified = models.DateTimeField(auto_now=True)
  modified_by = models.IntegerField(null=True, blank=True)
  status = models.BooleanField(default=True)

  class Meta:
    abstract = True

# Create your models here.
class Venue(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    capacity = models.IntegerField()
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Event(BaseModel):
    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    expected_guests = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default='pending')

    def clean(self):
        """
        Ensure that no other approved event exists for the same venue on the same date.
        Prevents multiple bookings at the same venue and time.
        """
        if self.venue:
            # Check if an event is already approved for this venue on the same date
            conflicting_event = Event.objects.filter(
                venue=self.venue,
                date__date=self.date.date(),  # Compare only the date (ignore time)
                approval_status='approved'
            ).exclude(id=self.id).exists()

            if conflicting_event:
                raise ValidationError("This venue is already booked for the selected date.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.date.strftime('%Y-%m-%d %H:%M')})"

   
class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class EventFood(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.event.name} - {self.food.name} ({self.quantity})" 
    
# class Booking(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     num_people = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.user.username} booked {self.num_people} for {self.event.name}"
   


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue', 'approval_status', 'created_by')
    list_filter = ('approval_status', 'date', 'venue')
    actions = ['approve_events', 'reject_events']

    def approve_events(self, request, queryset):
        queryset.update(approval_status='approved')
    approve_events.short_description = "Approve selected events"

    def reject_events(self, request, queryset):
        queryset.update(approval_status='rejected')
    reject_events.short_description = "Reject selected events"


