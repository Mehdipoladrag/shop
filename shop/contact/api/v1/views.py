from rest_framework import mixins, generics
from rest_framework.permissions import IsAdminUser
from contact.models import Contact
from .serializers import ContactSerializer


class ContactListMixin(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    This is a contact Api List
    For messages From all Users
    """

    queryset = Contact.objects.all().order_by("name")
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class ContactDetailMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    This is a contact Api Detail
    For messages From 1 User
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
