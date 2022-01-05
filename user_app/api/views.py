from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_app.api.permissions import IsOwnerOrReadOnly
from user_app.api.serializers import AccountSerializer, ChangePasswordSerializer, UserRegistrationSerializer, UserSerializer
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from user_app.models import Account
from rest_framework.decorators import api_view
from user_app.api.permissions import IsObjectOwner
class user_registration_view(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['fullname'] = self.user.fullname
        data['email'] = self.user.email
        data['phone'] = self.user.phone
        data['id']=self.user.id
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ChangePasswordView(generics.UpdateAPIView):
    queryset=Account.objects.all()
    permission_classes=[IsAuthenticated,IsObjectOwner,]
    serializer_class = ChangePasswordSerializer

class UserSearchListView(generics.ListAPIView):
    queryset=Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends=(filters.DjangoFilterBackend, SearchFilter,)
    filter_fields = ('username',)
    search_fields=('fullname',)

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

# class UserProfileChangeAPIView(generics.RetrieveAPIView,
#                                mixins.DestroyModelMixin,
#                                mixins.UpdateModelMixin):
#     permission_classes = (
#         permissions.IsAuthenticated,
#         UserIsOwnerOrReadOnly,
#     )
#     serializer_class = UserProfileChangeSerializer
#     parser_classes = (MultiPartParser, FormParser,)

#     def get_object(self):
#         user = self.kwargs["user"]
#         obj = get_object_or_404(Account, username=user)
#         return obj

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)