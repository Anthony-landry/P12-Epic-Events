from rest_framework import viewsets

from accounts.permissions import IsManagerPermission, IsSalesPermission, IsSupportPermission
from contracts.models import Contract
from contracts.serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsManagerPermission | IsSalesPermission, ]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsManagerPermission | IsSalesPermission | IsSupportPermission, ]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsManagerPermission | IsSalesPermission, ]
        elif self.action == 'destroy':
            permission_classes = [IsManagerPermission, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Les managers peuvent accéder à tous les contrats pour toute action
        if self.request.user.group.name == "Gestion":
            return Contract.objects.all()

        # Tout le monde peut accéder à tous les contrats en en lecture seule
        if self.action == 'list' or self.action =='retrieve':
            return Contract.objects.all()

        # Accès restreint pour la modification
        elif self.action == 'update' or self.action == 'partial_update':
            if self.request.user.group.name == "Vente":
                # Le membre de la vente a accès qu'aux contrats qu'il gère

                # On utilise le related name "contracts_handled_by_the_sales_contact" dans le champ "sales_contact" du modèle Contract
                # Cela nous permet d'accéder aux contrats gérés par le sales_contact (qui est un user donc un request.user!)
                # Pour cela, il faut faire : request.user.contracts_handled_by_the_sales_contact
                # related_name est très utile quand un champ Foreign Key apparait que dans un modèle (ici, Contract)
                # alors que ça lie bien deux modèles (ici, Contract et CustomUser)
                return self.request.user.contracts_handled_by_the_sales_contact

            # Pas besoin de checker le Support puisqu'elle n'a pas accès à la modification (cf permissions)
            else:
                # Si un nouveau groupe est créé et qu'on ne rentre pas dans les if,
                # il ne faut rien retourner : pas de faille de sécurité
                return None
        # Si c'est une autre action et qu'on ne rentre pas dans les if,
        # il ne faut rien retourner : pas de faille de sécurité
        return None
