from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="watchlist")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.listing}"

    def get_absolute_url(self):
        return reverse("listing", args=[str(self.listing.id)])

    def get_absolute_url_rem(self):
        return reverse("remove_watchlist", args=[str(self.listing.id)])


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    starting_bid = models.FloatField()
    image_url = models.CharField(max_length=100, blank=True)
    # category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="listings", blank=True)
    category = models.CharField(max_length=64, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", blank=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("listing", args=[str(self.id)])

    def get_absolute_url_add(self):
        return reverse("add_watchlist", args=[str(self.id)])


# class Category(models.Model):
#     name = models.CharField(max_length=64)

#     def __str__(self):
#         return f"{self.name}"

#     def get_absolute_url(self):
#         return reverse("category", args=[str(self.id)])


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
