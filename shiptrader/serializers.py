from rest_framework import serializers

from shiptrader.models import Starship, Listing


class StarShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
