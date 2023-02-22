from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user} {self.listing}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    starting_bid = models.FloatField()
    image_url = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=64, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", blank=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("listing", args=[str(self.id)])


class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid}"


class Comment(models.Model):
    comment = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.comment}"
