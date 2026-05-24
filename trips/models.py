from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):

    from_city = models.CharField(max_length=100)

    to_city = models.CharField(max_length=100)

    people = models.IntegerField()

    trip_date = models.DateField()

    total_budget = models.FloatField()

    def __str__(self):
        return f"{self.from_city} to {self.to_city}"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
