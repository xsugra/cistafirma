from django.contrib import admin
from .models import Address, Company


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Správa adries.
    """
    list_display = (
        'street',
        'city',
        'zip_code',
    )

    search_fields = (
        'city',
        'street',
        'zip_code',
    )

    list_filter = ('city',)
    ordering = ('city', 'street')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Hlavný prehľad firiem.
    """
    list_display = (
        'name',
        'ico',
        'get_city',
        'status',
        'created_at',
    )

    list_filter = ('status', 'created_at')

    search_fields = (
        'name',
        'ico',
        'address__city',
        'address__street',
    )

    list_select_related = ('address',)

    autocomplete_fields = ['address']


# Vlastná metóda na zobrazenie mesta z prepojenej tabuľky
    @admin.display(description='Sídlo')
    def get_city(self, obj):
        return obj.address.city if obj.address else "-"
