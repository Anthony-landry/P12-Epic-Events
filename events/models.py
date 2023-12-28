from django.db import models

from accounts.models import Client, CustomUser


# event_status = models.CharField(max_length=20, choices=(("created", 'Created'),
#                                                         ("in_progress", 'In progress'),
#                                                         ("finished", 'Finished'),
#                                                         )
#                                 )

# Statut à créer pour les différents évènements (Foreign key dans l'énoncé plutôt qu'un champ charfield avec des choices
# Signifique qu'on veut plus de flexibilité sur le statut
# puisqu'on a aucune info dessus dans l'énoncé d'où le modèle Status
class EventStatus(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "EventStatus"


class Event(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    # CASCADE car si on supprime un client, on veut que l'évènement soit supprimé
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING,
                                        related_name="events_handled_by_this_support_contact")
    event_status = models.ForeignKey(to=EventStatus, on_delete=models.DO_NOTHING)
    # DO_NOTHING car si on supprime un statut, on ne veut pas que l'évènement soit supprimé
    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Évènement {self.id} (Client {self.client.last_name}"
