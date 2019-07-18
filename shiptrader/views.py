from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarShipSerializer, ListingSerializer


class ShipTraderAPI(APIView, PageNumberPagination):
    def get_sorting(self):
        """
        Get sorting from query string, and return list of values to be
        used by order_by.
        Return None if no sorting is specified.
        """
        params = self.request.query_params
        asc = params.get('sort_asc')
        desc = params.get('sort_desc')
        if not asc and not desc:
            return None
        ordering = []
        if asc:
            ordering.append(asc)
        if desc:
            ordering.append('-{}'.format(desc))
        return ordering


class StarShipsAPI(ShipTraderAPI):
    page_size = 10

    def get(self, request):
        # Filter by starship class, if one is specified
        starship_class = request.query_params.get('class')
        if starship_class:
            queryset = Starship.objects.filter(starship_class=starship_class)
        else:
            queryset = Starship.objects.all()

        # Apply sorting to queryset
        sorting = self.get_sorting()
        if sorting:
            queryset = queryset.order_by(*sorting)

        results = self.paginate_queryset(queryset, request, self)
        serializer = StarShipSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = StarShipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StarShipAPI(APIView):
    def get(self, request, ship_id):
        ship = Starship.objects.get(id=ship_id)
        serializer = StarShipSerializer(ship)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, ship_id):
        ship = Starship.objects.get(id=ship_id)
        ship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListingsAPI(ShipTraderAPI):
    page_size = 10

    def get(self, request):
        queryset = Listing.objects.all()

        sorting = self.get_sorting()
        if sorting:
            queryset = queryset.order_by(*sorting)

        results = self.paginate_queryset(queryset, request, self)
        serializer = ListingSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingAPI(APIView):
    def get(self, request, listing_id):
        listing = Listing.objects.get(id=listing_id)
        serializer = ListingSerializer(listing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, listing_id):
        listing = Listing.objects.get(id=listing_id)
        listing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListingAPIActions(APIView):
    def patch(self, request, listing_id, action):
        listing = Listing.objects.get(id=listing_id)
        if action == 'activate':
            listing.active = True
            listing.save()
        if action == 'deactivate':
            listing.active = False
            listing.save()
        serializer = ListingSerializer(listing)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExecuteOrder66(APIView):
    def delete(self, request):
        """
        Do it.
        """
        Starship.objects.all().delete()
        Listing.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
