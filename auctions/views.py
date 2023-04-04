from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import *
from .models import User


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    # display starting bid as currency
    currency = "${:,.2f}".format(listing.starting_bid)
    listing.starting_bid = currency

    return render(request, "listing.html", {
        "listing": listing,
    })


def index(request):
    listings = Listing.objects.all()

    # clean up image urls
    for listing in listings:
        if listing.image_url == "":
            listing.image_url = "https://via.placeholder.com/150"

    # convert starting bid to currency
    for listing in listings:
        currency = "${:,.2f}".format(listing.starting_bid)
        listing.starting_bid = currency


    return render(request, "index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    categories = [category for category in categories if category != ""]

    return render(request, "categories.html", {
        "categories": categories,
    })


def listings_by_category(request, category_name):
    listing_by_category = Listing.objects.filter(category__exact=category_name)

    return render(request, "listings_by_category.html", {
        "listings": listing_by_category,
        "category_name": category_name,
    })


@login_required
def watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)

    return render(request, "watchlist.html", {
        "watchlist": watchlist,
    })


@login_required
def add_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    if Watchlist.objects.filter(user=user, listing=listing).exists():
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        Watchlist.objects.create(user=user, listing=listing)
        return HttpResponseRedirect(reverse("watchlist"))


@login_required
def remove_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.filter(user=user, listing=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def create_listing(request):
    user = request.user
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.cleaned_data
            listing = Listing.objects.create(
                title=listing['title'],
                description=listing['description'],
                starting_bid=listing['starting_bid'],
                image_url=listing['image_url'],
                category=listing['category'],
                user=user
            )
            return HttpResponseRedirect('/listing/' + str(listing.id))
    else:
        form = CreateListingForm()

    return render(request, 'create.html', {'form': form})


def error404(request, exception):
    return render(
        request,
        "404.html",
        status=404
    )
