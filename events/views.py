from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from accounts.permissions import IsManagerPermission, IsSalesPermission, IsSupportPermission
from events.models import Event
from events.serializers import EventSerializer
from .filters import EventFilter


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsManagerPermission | IsSalesPermission, ]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsManagerPermission | IsSalesPermission | IsSupportPermission, ]
        elif self.action == 'update' or self.action == 'partial_update':
            # C'est assez bizarre que la Vente crée des évènements mais ne puisse pas les modifier
            # (cas où la vente fait une erreur par exemple) mais c'est pas marqué que la Vente peut modifier
            # Donc si on respecte à la règle, seul le support peut modifier.
            # La vente crée et le support modifie sans avoir créé
            permission_classes = [IsManagerPermission | IsSupportPermission, ]
        elif self.action == 'destroy':
            permission_classes = [IsManagerPermission, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Les managers peuvent accéder à tous les évènements pour toute action
        if self.request.user.group.name == "Gestion":
            return Event.objects.all()

        # Tout le monde peut accéder à tous les évènements en en lecture seule
        if self.action == 'list' or self.action == 'retrieve':
            return Event.objects.all()

        # Accès restreint pour la modification
        elif self.action == 'update' or self.action == 'partial_update':
            if self.request.user.group.name == "Support":
                # Le membre du support a accès qu'aux évènements qu'il gère

                # On utilise le related name "events_handled_by_this_support_contact"
                # dans le champ "support_contact" du modèle Event
                # Cela nous permet d'accéder aux évènements gérés par le support_contact
                # (qui est un user donc un request.user!)
                # Pour cela, il faut faire : request.user.events_handled_by_this_support_contact
                # related_name est très utile quand un champ Foreign Key apparait que dans un modèle (ici, Event)
                # alors que ça lie bien deux modèles (ici, Event et CustomUser)
                return self.request.user.events_handled_by_this_support_contact

            # Pas besoin de checker la Vente puisqu'elle n'a pas accès à la modification (cf permissions)
            else:
                # Si un nouveau groupe est créé et qu'on ne rentre pas dans les if,
                # il ne faut rien retourner : pas de faille de sécurité
                return None
        # Si c'est une autre action et qu'on ne rentre pas dans les if,
        # il ne faut rien retourner : pas de faille de sécurité
        return None
