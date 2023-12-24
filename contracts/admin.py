from django.contrib import admin

from contracts.forms import ContractForm
from contracts.models import Contract


class ContractAdmin(admin.ModelAdmin):
    form = ContractForm
    ordering = ("-id",) # Ordonner les contrats par id par ordre décroissant pour avoir les plus récents en haut
    list_display = ('client', 'id') # Informations qui seront affichées dans la rubrique contrats

# Register your models here.
admin.site.register(Contract, ContractAdmin)