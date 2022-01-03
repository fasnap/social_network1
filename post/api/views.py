from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from post.api.serializers import  PostSerializer
from post.models import Comment, Post
from rest_framework import generics, serializers
from rest_framework import permissions
from rest_framework.response import Response
from post.api.permissions import OwnerOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import CommentSerializer

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          OwnerOnly,]

class AddLikeUnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,post_id):
        post=Post.objects.get(pk=post_id)
        if post.liked_by.filter(pk=request.user.pk).exists():
            post.liked_by.remove(request.user)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            post.liked_by.add(request.user)
            return Response(status=status.HTTP_200_OK)

class PostListAV(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = (MultiPartParser, FormParser)
    def get(self,request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetailAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(OwnerOnly,permissions.IsAuthenticated,)
    serializer_class=PostSerializer
    queryset=Post.objects.all()
   
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
