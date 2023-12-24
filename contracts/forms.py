from django import forms
from django.contrib.auth.models import Group

from contracts.models import Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restreindre le queryset pour le champ "sales_contact" aux utilisateurs qui sont dans le groupe "Vente"
        sales_group = Group.objects.get(name="Vente")
        self.fields["sales_contact"].queryset = sales_group.user_set.all()
