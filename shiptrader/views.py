from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarShipSerializer, ListingSerializer


class StarShipsAPI(APIView, PageNumberPagination):
    page_size = 10

    def get(self, request):
        queryset = Starship.objects.all()
        results = self.paginate_queryset(queryset, request, self)
        serializer = StarShipSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = StarShipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class ListingsAPI(APIView, PageNumberPagination):
    page_size = 10

    def get(self, request):
        queryset = Listing.objects.all()
        results = self.paginate_queryset(queryset, request, self)
        serializer = ListingSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    def get(self, request, listing_id, action):
        pass
