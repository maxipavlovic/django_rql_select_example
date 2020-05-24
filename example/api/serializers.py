from rest_framework import serializers

from dj_rql.drf.serializers import RQLMixin

from ..models import Category, Company, Product


class CategorySerializer(RQLMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CompanySerializer(RQLMixin, serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class ProductSerializer(RQLMixin, serializers.ModelSerializer):
    category = CategorySerializer()
    company = CompanySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'company')

