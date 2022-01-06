
from django.urls import path
from rest_framework import views
from .views import AddLikeUnlikeView, PostDetailAV,PostListAV,AddCommentView,ManageCommentView

urlpatterns = [
    path('posts/', PostListAV.as_view()),
    path('<int:pk>/',PostDetailAV.as_view(),name='post-detail'),  
    # path('comment_create/',CreateCommentView.as_view(),name='comment-create'),
    path('comments/<int:post_id>/',AddCommentView.as_view(),name='add-comment'),
    path('comment/<int:comment_id>/',ManageCommentView.as_view(),name='manage-comment'),
    path('like/unlike/<int:post_id>/', AddLikeUnlikeView.as_view(), name='like_unlike'),
    # path('updatePost/<int:pk>/',PostDetailAV.as_view(), name='update-post'),
    # path('deletePost/<int:pk>/',PostDetailAV.as_view(), name='delete-post'),
    # path('comments/', CommentList.as_view()),
    # path('comments/<int:pk>/', CommentDetail.as_view()),
]