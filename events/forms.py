from django import forms
from django.contrib.auth.models import Group

from events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restreindre le queryset pour le champ "sales_contact" aux utilisateurs qui sont dans le groupe "Vente"
        support_group = Group.objects.get(name="Support")
        self.fields["support_contact"].queryset = support_group.user_set.all()
