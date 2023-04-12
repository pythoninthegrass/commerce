#!/usr/bin/env python3

# fmt: off
from datetime import timedelta
from django_seed import Seed
from decouple import config
from pathlib import Path
# fmt: on

# TODO: models.py `ModuleNotFoundError: No module named 'auctions.settings'`
django_settings_module = config("DJANGO_SETTINGS_MODULE")
if django_settings_module == "auctions.settings":
    from auctions.models import User, Listing, Bid, Comment, Watchlist

seeder = Seed.seeder()

seeder.add_entity(User, 5, {
    'is_staff': False,
    'is_superuser': False,
})

seeder.add_entity(Listing, 5, {
    'title': lambda x: seeder.faker.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None),
    'description': lambda x: seeder.faker.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None),
    'starting_bid': lambda x: seeder.faker.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=0, max_value=1000),
    'image_url': lambda x: seeder.faker.image_url(width=640, height=480, category='abstract'),
    'category': lambda x: seeder.faker.word(ext_word_list=None),
    'user': lambda x: seeder.faker.random_element(elements=(User.objects.all())),
})

seeder.add_entity(Bid, 5, {
    'bid': lambda x: seeder.faker.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=0, max_value=1000),
    'user': lambda x: seeder.faker.random_element(elements=(User.objects.all())),
    'listing': lambda x: seeder.faker.random_element(elements=(Listing.objects.all())),
})

seeder.add_entity(Comment, 5, {
    'comment': lambda x: seeder.faker.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None),
    'user': lambda x: seeder.faker.random_element(elements=(User.objects.all())),
    'listing': lambda x: seeder.faker.random_element(elements=(Listing.objects.all())),
})

seeder.add_entity(Watchlist, 5, {
    'user': lambda x: seeder.faker.random_element(elements=(User.objects.all())),
    'listing': lambda x: seeder.faker.random_element(elements=(Listing.objects.all())),
})

inserted_pks = seeder.execute()
