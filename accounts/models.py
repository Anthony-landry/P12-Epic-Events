from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):


    def create_superuser(self, email, first_name, last_name, password, **kwargs):

        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True

        try:
            gestion_group = Group.objects.get(name="Gestion")
        except:
            gestion_group = Group.objects.create(name="Gestion")
        try:
            vente_group = Group.objects.get(name="Vente")
        except:
            vente_group = Group.objects.create(name="Vente")
        try:
            support_group = Group.objects.get(name="Support")
        except:
            support_group = Group.objects.create(name="Support")

        # On met automatiquement tous les superusers dans le groupe Gestion

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, group=gestion_group, **kwargs)
        user.set_password(password)
        user.save()



# Personnalisation du modèle User de Django pour ajouter l'appartenance à un groupe Django
class CustomUser(AbstractUser):

    username = None # On utilisera l'email plutôt que le username
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")

    # On associe un groupe à chaque utilisateur
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name="custom_users_in_the_group")
    # DO_NOTHING et pas CASCADE car on ne veut pas que l'utilisateur (CustomUser) soit supprimé si un groupe est supprimé

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()

    def __str__(self):
        return f"Utilisateur : {self.email}"

    def save(self, *args, **kwargs):
        print("I'm in the save method")

        # Attribution des permissions correspondantes
        if self.group.name == "Gestion":

            self.is_staff = True
            self.is_superuser = True
            self.is_active = True

        elif self.group.name == "Vente" or self.group.name == "Support":
            self.is_staff = False
            self.is_superuser = False
            self.is_active = True

        super().save(*args, **kwargs)
@receiver(post_save, sender=CustomUser)
def add_to_group(instance, **kwargs):
    # Ajouter l'utilisateur au groupe Django qui est selectionné à chaque sauvegarde.
    # En effet, sans ceci, le group est simplement sélectionné pour le CustomUser mais il n'est pas ajouté pour de vrai dans un groupe Django

    # On utilise le signal "post_save" car on ne peut pas le faire dans la méthode save à la création d'un objet
    # En effet, on ne peut pas ajouter un utilisateur pas encore créé, ce dernier est créé qu'après le save()
    # Donc à chaque save, cette fonction est appelée

    instance.group.user_set.add(instance)

class Client(models.Model):
    first_name = models.CharField(max_length=25, verbose_name="First Name")
    last_name = models.CharField(max_length=25, verbose_name="Last Name")
    email = models.EmailField(max_length=100, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    mobile = models.CharField(max_length=20, verbose_name="Mobile")
    company_name = models.CharField(max_length=250, verbose_name="Company Name")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(to=CustomUser, on_delete=models.DO_NOTHING, related_name="clients_represented_by_this_sales_contact")
    # DO_NOTHING et pas CASCADE car on ne veut pas que le client soit supprimé si l'utilisateur est supprimé

    def __str__(self):
        return f"Client {self.first_name} {self.last_name}"
