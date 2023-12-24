from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import ClientForm
from accounts.models import CustomUser, Client


class CustomUserAdmin(UserAdmin):

    ordering = ("-id",) # Ordonner les utilisateurs par id par ordre décroissant pour avoir les plus récents en haut
    list_display = ('email', 'group', 'id') # Informations qui seront affichées dans la rubrique utilisateurs
    list_filter = ('group',) # Pour filter par groupe

    # Personnalisation des champs apparaissant lorsqu'on clique sur un utilisateur
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User information', {'fields': ('first_name', 'last_name', 'group', 'date_joined')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'group'),
        }),
    )

# Enregistrement du modèle utilisateur personnalisé (CustomUser) et de la classe CustomUserAdmin gérant son affichage dans l'admin
admin.site.register(CustomUser, CustomUserAdmin)

class ClientAdmin(admin.ModelAdmin):
    ordering = ("-id",) # Ordonner les clients par id par ordre décroissant pour avoir les plus récents en haut
    list_display = ('email', 'id') # Informations qui seront affichées dans la rubrique clients
    form = ClientForm

admin.site.register(Client, ClientAdmin)
