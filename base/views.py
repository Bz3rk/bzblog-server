from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import ClientRegistrationSerializer, DataSerializer, BlogSerializer, TopicSerializer
from .models import CustomUser, Blog, Topic

# Create your views here.


# @extend_schema(request = ClientRegistrationSerializer, responses = ClientRegistrationSerializer)
@api_view(['POST'])
def ClientRegister(request):
    if request.method == 'POST':
        serializer = ClientRegistrationSerializer(data=request.data, many=False)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({"userData": serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response({'Errors': serializer.errors})
    return Response({})


@api_view([ 'POST'])
def ClientLogin(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message": "Invalid credentials..."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({"message": "Invalid credentials..."}, status=status.HTTP_400_BAD_REQUEST)
            
        token, created = Token.objects.get_or_create(user=user)
        serializer = DataSerializer(instance=user)
        # print (email)
        # print(password)
        return Response({'userData': serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
    return Response({})

            

class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    


class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    

class BlogDeleteView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]


class BlogUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    partial = True
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]
