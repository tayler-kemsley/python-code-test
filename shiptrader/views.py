from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class StarShipsAPI(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class StarShipAPI(APIView):
    def get(self, request, ship_id):
        pass

    def delete(self, request, ship_id):
        pass


class ListingsAPI(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class ListingAPI(APIView):
    def get(self, request, ship_id):
        pass

    def delete(self, request, ship_id):
        pass
