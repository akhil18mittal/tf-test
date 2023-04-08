from django.db import models
# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    borrower = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.borrower} - {self.amount} - {self.country} - {self.sector} - {self.year}"
