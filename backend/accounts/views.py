'''
This script include User Management

-----> features <----
- user registration
- user login
- user search

'''


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


#  serializers 
from .serializers import RegisterSerializer, UserSerializer

# models
from .models import User
# Create your views here.




# user sign up view or register view
class RegisterView(APIView):

    '''User sign up view creates new user '''
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
                return Response(content, 
                                status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            print('working')
            if 'password' in str(e):
                return Response({'message': e},
                                status=status.HTTP_400_BAD_REQUEST)
            print(e)
            return Response({'message': 'Something went wrong'},
                             status=status.HTTP_400_BAD_REQUEST)



#  user login view 
class LoginView(APIView):
    """
    Handles user login and returns JWT tokens upon successful authentication.
    """

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if email is None or password is None:
                return Response({'message':"Please provide both email and password"},
                                status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # check the user is blocked or not
                if not user.is_active:  
                    return Response({"message":"You account is blocked"}, 
                                    status=status.HTTP_403_FORBIDDEN)
                
                refresh = RefreshToken.for_user(user) # generating new refresh token for the user
                refresh["username"] = str(user.username) # custom cliam in the acess token
                
                content = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
                    }

                return Response(content,status=status.HTTP_200_OK)
            else:
                return Response({'message':"Invalid credentials"},
                                 status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({'message': "An error occurred. Please try again later."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', "")
        page_number = request.query_params.get('page', 1)
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) | Q(email__iexact=query)
            )

            paginator = Paginator(users, 10)  # 10 items per page
            try:
                users_paginated = paginator.page(page_number)
            except PageNotAnInteger:
                users_paginated = paginator.page(1)
            except EmptyPage:
                users_paginated = paginator.page(paginator.num_pages)

            serializer = UserSerializer(users_paginated, many=True)
            return Response(serializer.data,
                             status=status.HTTP_200_OK)

        return Response({'error': 'Query parameter is missing'},
                         status=status.HTTP_400_BAD_REQUEST)
