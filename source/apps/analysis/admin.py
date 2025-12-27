from django.contrib import admin
from .models import Debt, VatStatus, RiskScore


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    """
    Prehľad dlhov firmy.
    """
    list_display = (
        'company',
        'source',
        'amount_eur',
        'date_of_record',
        'created_at'
    )

    list_filter = (
        'source',
        'date_of_record',
    )

    search_fields = (
        'company__name',
        'source',
        'amount_eur',
    )

    ordering = ('-created_at',)


@admin.register(VatStatus)
class VatStatusAdmin(admin.ModelAdmin):
    """
    DPH status firmy.
    """
    list_display = (
        'company',
        'tax_reliability_index',
        'updated_at',
    )

    list_filter = ('tax_reliability_index',)
    search_fields = ('company__name',)


@admin.register(RiskScore)
class RiskScoreAdmin(admin.ModelAdmin):
    """
    Prehľad rizikového skóre firmy.
    """
    list_display = (
        'company',
        'score',
        'calculation_date',
    )

    list_filter = ('calculation_date',)
    search_fields = ('company__name',)
