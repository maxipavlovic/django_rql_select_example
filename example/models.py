from django.db import models


class StrMixin:
    def __str__(self):
        return self.name


class Category(StrMixin, models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Categories'


class Company(StrMixin, models.Model):
    name = models.CharField(max_length=32, db_index=True)

    class Meta:
        verbose_name_plural = 'Companies'


class Product(StrMixin, models.Model):
    name = models.CharField(max_length=32, db_index=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
