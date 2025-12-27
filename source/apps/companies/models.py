import uuid
from django.db import models


# Model adresy pre firmu
class Address(models.Model):
    """
    Model reprezentujúci adresu firmy (tabuľka: companies_address).
    companies_company 1 : N companies_address
    Jedna firma má jedno sídlo, na jednej adrese môže sídliť viacero firiem.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    street = models.CharField(max_length=255, verbose_name="Ulica a číslo")

    city = models.CharField(max_length=255, verbose_name="Mesto")

    zip_code = models.CharField(max_length=10, verbose_name="PSČ")

    country = models.CharField(max_length=50, verbose_name="Krajina")

    class Meta:
        db_table = 'companies_address'
        verbose_name = 'Adresa'
        verbose_name_plural = 'Adresy'

    def __str__(self):
        return f"{self.street}, {self.city}"


# Model Firmy
class Company(models.Model):
    """
    Model reprezentujúci Firmu (tabuľka: companies_company).
    companies_company 1 : N companies_address
    Jedna firma má jedno sídlo, na jednej adrese môže sídliť viacero firiem.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )

    ico = models.CharField(max_length=8, unique=True, verbose_name="IČO")

    name = models.CharField(max_length=255, verbose_name="Obchodný názov")

    legal_form = models.CharField(max_length=100, verbose_name="Právna forma")

    status = models.CharField(max_length=50, verbose_name="Status")

    registration_date = models.DateField(verbose_name="Dátum vzniku")

    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,  # Nedovolíme zmazať adresu, ak na nej sídli nejaká firma
        related_name='companies',  # Umožní získať všetky firmy na danej adrese (address.companies.all())
        verbose_name="Sídlo"
    )

    last_updated_from_source = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Naposledy synchronizované"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vytvorené")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Upravené")

    class Meta:
        db_table = 'companies_company'
        verbose_name = 'Firma'
        verbose_name_plural = 'Firmy'

    def __str__(self):
        return self.name
