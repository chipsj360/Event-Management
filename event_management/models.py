from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    expected_guests = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
   
class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
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
    
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.num_people} for {self.event.name}"