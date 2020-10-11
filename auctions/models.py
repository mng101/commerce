from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=32)
    date_listed = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    image = models.URLField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.title} - {self.category} - $ {self.starting_bid}"

    def get_absolute_url(self):
        return reverse("detail", kwargs={'pk':self.pk})