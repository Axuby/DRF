from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.api.serializers import LoginSerializer, ManageUserSerializer, RegistrationSerializer
from account.models import Account


@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def reqistration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = {}
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            # password2 = serializer.validated_data.get("password2")
            account = User.objects.create(username=username, email=email)
            account.set_password(password)
            account.save()

            data["response"] = "Registration successful!"
            data["first_name"] = account.first_name
            data["last_name"] = account.last_name
            data["username"] = account.username
            data["email"] = account.email
            refresh_token = RefreshToken.for_user(account)
            data["refresh_token"] = str(refresh_token)
            data["access_token"] = str(refresh_token.access_token)

            # token, created = Token.objects.get_or_create(user=account)
            # data["token"] = token.key

            return Response(data)
            # return Response(serializer.data)
        data = serializer.errors
        return Response(data)


# class RegisterView(CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer


class CustomLoginToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        print("Here")
        if not serializer.is_valid():
            print("Here")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = login(username, password)
            print(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                # {
                # 'token': token.key,
                # 'username': username,
                # 'user_id': user.pk,
                # 'email': user.email
                # }
            )
        else:
            return Response(serializer.errors)


class LoginToken(ObtainAuthToken):
    serializer_class = LoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    serializer_class = ManageUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
