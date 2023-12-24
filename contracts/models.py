from django.db import models

from accounts.models import CustomUser, Client


class Contract(models.Model):
    sales_contact = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING, related_name="contracts_handled_by_the_sales_contact")
    # DO_NOTHING et pas CASCADE car on ne veut pas que le client soit supprimé si l'utilisateur est supprimé
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name="contracts_associated_to_this_client")
    # CASCADE car si on supprime un client, on veut que le contrat soit supprimé
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    amount = models.FloatField(default=0.0)
    payment_due = models.DateTimeField()

    def __str__(self):
        return f"Contrat {self.id} (Client {self.client.last_name}"
