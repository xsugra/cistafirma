import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


# Model reprezentujúci dlh firmy
class Debt(models.Model):
    """
    Model reprezentujúci dlh firmy (tabuľka: analysis_debt).
    companies_company 1 : N analysis_debt
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,  # Ak vymažeme Firmu z databázy, automaticky vymaž aj všetky jej Dlhy.
        related_name='debts',
    )

    source = models.CharField(
        max_length=50,
        verbose_name="Zdroj dlhu",
    )

    amount_eur = models.DecimalField(  # Decimal ukladá čísla ako text - matematickú štruktúru.
        max_digits=12,
        decimal_places=2,
        verbose_name="Suma v EUR",
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )

    date_of_record = models.DateField(
        verbose_name="Dátum evidencie",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Vytvorené v DB",
    )

    class Meta:
        db_table = 'analysis_debt'
        verbose_name = 'Dlh',
        verbose_name_plural = 'Dlhy',
        indexes = [
            models.Index(fields=['company', 'date_of_record']),
        ]

    def __str__(self):
        return f"{self.source}: {self.amount_eur} EUR"


# Model pre DPH status firmy
class VatStatus(models.Model):
    """
    Model pre DPH status firmy (tabuľka: analysis_vatstatus).
    companies_company 1 : 1 analysis_vatstatus
    Jedna firma má práve jeden aktuálny status.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    company = models.OneToOneField(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='vat_status',
    )

    # Príklad: "SPOĽAHLIVÝ", "NESPOĽAHLIVÝ", "NA PREVERENIE"
    tax_reliability_index = models.CharField(
        max_length=50,
        verbose_name="Index daňovej spoľahlivosti",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Naposledy overené",
    )

    class Meta:
        db_table = 'analysis_vatstatus'
        verbose_name = 'DPH Status'
        verbose_name_plural = 'DPH Statusy'

    def __str__(self):
        return f"{self.company}: {self.tax_reliability_index}"


# Model pre históriu rizikového skóre
class RiskScore(models.Model):
    """
    Model pre históriu rizikového skóre (tabuľka: analysis_riskscore).
    companies_company 1 : N analysis_riskscore
    Jedna firma má veľa záznamov o skóre v čase.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='risk_scores',
    )

    score = models.IntegerField(
        verbose_name="Skóre",
    )

    calculation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Dátum výpočtu",
    )

    class Meta:
        db_table = 'analysis_riskscore'
        verbose_name = 'Rizikové skóre'
        verbose_name_plural = 'História rizikového skóre'
        # UX/DB Tip: Defaultne zoraďujeme od najnovšieho po najstaršie
        ordering = ['-calculation_date']
        indexes = [
            models.Index(fields=['company', 'calculation_date']),
        ]

    def __str__(self):
        return f"{self.company}: {self.score} ({self.calculation_date.strftime('%Y-%m-%d')})"
