from .models import Institution, Category
from rest_framework import serializers


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Category)

    class Meta:
        model = Institution
        fields = ("id", "name", "description", "type", "categories")
