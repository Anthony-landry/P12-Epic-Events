from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import viewsets, status
from rest_framework.response import Response

from accounts.models import Client
from accounts.permissions import IsManagerPermission, IsSalesPermission, IsSupportPermission
from accounts.serializers import UserSerializer, ClientSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManagerPermission]

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    # queryset = Client.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            # "|" pour l'un ou l'autre, si "," : il faudrait les deux permissions
            permission_classes = [IsManagerPermission | IsSalesPermission, ]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsManagerPermission | IsSalesPermission | IsSupportPermission, ]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsManagerPermission | IsSalesPermission, ]
        elif self.action == 'destroy':
            permission_classes = [IsManagerPermission, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Les managers peuvent accéder à tous les clients pour toute action
        if self.request.user.group.name == "Gestion":
            return Client.objects.all()

        # Tout le monde peut accéder à tous les clients en en lecture seule
        if self.action == 'list' or self.action == 'retrieve':
            return Client.objects.all()

        # Accès restreint pour la modification
        elif self.action == 'update' or self.action == 'partial_update':
            if self.request.user.group.name == "Vente":
                return self.request.user.clients_represented_by_this_sales_contact
            # Pas besoin de checker le Support puisqu'il n'a pas accès à la modification ou la suppression (cf permissions)
            else:
                # Si un nouveau groupe est créé et qu'on ne rentre pas dans les if,
                # il ne faut rien retourner : pas de faille de sécurité
                return None
        # Si c'est une autre action et qu'on ne rentre pas dans les if,
        # il ne faut rien retourner : pas de faille de sécurité
        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            # Restreindre le queryset pour le champ "sales_contact" aux utilisateurs qui sont dans le groupe "Vente"
            sales_group = Group.objects.get(name='Vente')
            serializer.fields['sales_contact'].queryset = sales_group.user_set.all()
            serializer.save()
            return Response({'message': "Le client a bien été créé"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     object_to_be_updated = self.get_object()
    #     if object_to_be_updated not in request.user.clients_represented_by_this_sales_contact.all():
    #         return Response({"détail": "Vous ne vous occupez pas de ce client"}, status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = self.get_serializer(object_to_be_updated, data=request.data, partial=False)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data)

