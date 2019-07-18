import json

from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from shiptrader.models import Starship, Listing
from shiptrader.views import StarShipsAPI, StarShipAPI, ListingsAPI, ListingAPI, ListingAPIActions


class TestStarshipViews(TransactionTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.new_ship_1 = {
            'model': 'Test model 1',
            'starship_class': 'Test class 1',
            'manufacturer': 'Test manufacturer 1',
            'length': 34456,
            'hyperdrive_rating': 1.3,
            'cargo_capacity': 86,
            'crew': 7,
            'passengers': 10
        }
        self.new_ship_2 = {
            'model': 'Test model',
            'starship_class': 'Test class',
            'manufacturer': 'Test manufacturer',
            'length': 2044,
            'hyperdrive_rating': 2.3,
            'cargo_capacity': 30,
            'crew': 2,
            'passengers': 1
        }

    def tearDown(self):
        Starship.objects.all().delete()

    def test_create_starship(self):
        request = self.factory.post(
            reverse('trader:starships'), self.new_ship_1, format='json'
        )
        view = StarShipsAPI.as_view()
        response = view(request)

        created_ship = Starship.objects.filter(**self.new_ship_1).exists()
        self.assertEqual(
            response.status_code,
            201
        )
        self.assertTrue(created_ship)

    def test_get_sorted_ships(self):
        ship_1 = Starship.objects.create(**self.new_ship_1)
        ship_2 = Starship.objects.create(**self.new_ship_2)

        # Test sort ascending
        request = self.factory.get(
            '{}?sort_asc=length'.format(reverse('trader:starships'))
        )
        view = StarShipsAPI.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], ship_2.id)

        # Test sort descending
        request = self.factory.get(
            '{}?sort_desc=length'.format(reverse('trader:starships'))
        )
        view = StarShipsAPI.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], ship_1.id)

    def test_delete_ship(self):
        ship_1 = Starship.objects.create(**self.new_ship_1)

        request = self.factory.delete(
            reverse('trader:starship', kwargs={'ship_id': ship_1.id})
        )
        view = StarShipAPI.as_view()
        response = view(request, ship_id=ship_1.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Starship.objects.filter(**self.new_ship_1).exists())


class TestListings(TransactionTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.ship_1 = Starship.objects.create(**{
            'model': 'Test model 1',
            'starship_class': 'Test class 1',
            'manufacturer': 'Test manufacturer 1',
            'length': 34456,
            'hyperdrive_rating': 1.3,
            'cargo_capacity': 86,
            'crew': 7,
            'passengers': 10
        })
        self.ship_2 = Starship.objects.create(**{
            'model': 'Test model',
            'starship_class': 'Test class',
            'manufacturer': 'Test manufacturer',
            'length': 2044,
            'hyperdrive_rating': 2.3,
            'cargo_capacity': 30,
            'crew': 2,
            'passengers': 1
        })
        self.listing_1 = {
            'name': 'Test listing',
            'ship_type': self.ship_1.id,
            'price': 10000
        }
        self.listing_2 = {
            'name': 'Test listing 2',
            'ship_type': self.ship_2.id,
            'price': 2000000
        }

    def tearDown(self):
        Starship.objects.all().delete()
        Listing.objects.all().delete()

    def test_create_listing(self):
        request = self.factory.post(
            reverse('trader:listings'), self.listing_1, format='json'
        )
        view = ListingsAPI.as_view()
        response = view(request)

        new_listing = Listing.objects.filter(**self.listing_1).exists()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(new_listing)

    def test_get_sorted_listings(self):
        self.listing_1['ship_type'] = self.ship_1
        self.listing_2['ship_type'] = self.ship_2
        listing_1 = Listing.objects.create(**self.listing_1)
        listing_2 = Listing.objects.create(**self.listing_2)

        # Test sort ascending
        request = self.factory.get(
            '{}?sort_asc=price'.format(reverse('trader:listings'))
        )
        view = ListingsAPI.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], listing_1.id)

        # Test sort descending
        request = self.factory.get(
            '{}?sort_desc=price'.format(reverse('trader:listings'))
        )
        view = ListingsAPI.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['id'], listing_2.id)

    def test_delete_listing(self):
        self.listing_1['ship_type'] = self.ship_1
        listing_1 = Listing.objects.create(**self.listing_1)

        request = self.factory.delete(
            reverse('trader:listing', kwargs={'listing_id': listing_1.id})
        )
        view = ListingAPI.as_view()
        response = view(request, listing_1.id)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Listing.objects.filter(**self.listing_1).exists())

    def test_activate_listing(self):
        self.listing_1['ship_type'] = self.ship_1
        listing_1 = Listing.objects.create(**self.listing_1)
        self.assertFalse(listing_1.active)

        request = self.factory.patch(
            reverse(
                'trader:listing-actions',
                kwargs={'listing_id': listing_1.id, 'action': 'activate'}
            )
        )
        view = ListingAPIActions.as_view()
        response = view(request, listing_1.id, 'activate')

        self.assertEqual(response.status_code, 200)
        activated_listing = Listing.objects.get(id=listing_1.id)
        self.assertTrue(activated_listing.active)

    def test_deactivate_listing(self):
        self.listing_1['ship_type'] = self.ship_1
        listing_1 = Listing.objects.create(**self.listing_1)
        listing_1.active = True
        listing_1.save()

        request = self.factory.patch(
            reverse(
                'trader:listing-actions',
                kwargs={'listing_id': listing_1.id, 'action': 'deactivate'}
            )
        )
        view = ListingAPIActions.as_view()
        response = view(request, listing_1.id, 'deactivate')

        self.assertEqual(response.status_code, 200)
        activated_listing = Listing.objects.get(id=listing_1.id)
        self.assertFalse(activated_listing.active)


