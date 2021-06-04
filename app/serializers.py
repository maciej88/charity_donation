from .models import Institution
from rest_framework import serializers

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ("id", "name", "description", "type", "categories")
