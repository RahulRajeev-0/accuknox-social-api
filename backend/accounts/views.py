from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#  serializers 
from .serializers import RegisterSerializer
# Create your views here.


class RegisterView(APIView):

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':"Registration Successfull"},
                                 status=status.HTTP_201_CREATED)
            else:
                error_messages = []
                for field, errors in serializer.errors.items():
                    for error in errors:
                        if field == 'email' and 'unique' in error:
                            error_messages.append("Email already exists")
                        else:
                            error_messages.append(f"{field.capitalize()}: {error}")
                
                content = {"message": error_messages}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            print('working')
            if 'password' in str(e):
                return Response({'message': e},
                                status=status.HTTP_400_BAD_REQUEST)
            print(e)
            return Response({'message': 'Something went wrong'},
                             status=status.HTTP_400_BAD_REQUEST)
