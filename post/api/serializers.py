
from post.models import Comment, Post
from rest_framework import serializers
from user_app.api.serializers import AccountSerializer
from user_app.models import Account
from django.core.paginator import Paginator
class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for object author info"""

    class Meta:
        model = Account
        fields = ['username','id']
class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author']
        required = ['body']
        read_only_fields = ('author', 'id', 'post_date')
        
class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    post_image=serializers.ImageField(max_length=None, allow_empty_file=False)
    post_comments = serializers.SerializerMethodField('paginated_post_comments')
    # comments = CommentSerializer(many=True, read_only=True)
    number_of_comments = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields = [
            "id",
            "author",
            "post_image",
            "title",
            "description",
            "total_likes",
            "number_of_comments",
            "post_comments",
            "liked_by",
        ]
    def get_total_likes(self,instance):
        return instance.liked_by.count()
    
    def paginated_post_comments(self, obj):
        post = Post.objects.get(pk=obj.id)
        post_comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(post_comments, many=True)

        return serializer.data
    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()

    def liked_by(self, obj):
        user = self.context['request'].user
        return user in obj.liked_by.all()



class PostUpdateSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model=Post
        fields = [
            "id",
            "author",
            "title",
            "description",
        ]
# class PostDeleteSerializer(serializers.ModelSerializer):
#     author = serializers.SerializerMethodField('author_id')
#     # author = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     class Meta:
#         model=Post
#         fields = [
#             "id",
#             "author",
#         ]

#     def author_id(self, obj):
#         author = self.context['request'].user
#         return Account.objects.filter(author=obj)


















       
    # @staticmethod
    # def get_likes_amount(obj):
    #     return obj.likes.count()

    # @staticmethod
    # def get_comments_amount(obj):
    #     return obj.comments.count()

    # def get_is_liked(self, obj):
    #     user = self.context['request'].user
    #     print (user)
    #     if user and not user.is_anonymous:
    #         return bool(obj.likes.filter(author=user))
    #     return None
# class LikesDetailedSerializer(serializers.ModelSerializer):
#     author = AccountSerializer(read_only=True)
#     post = PostSerializer(read_only=True)

#     class Meta:
#         model = Like
#         fields = "__all__"
#         extra_kwargs = {"author": {"read_only": True}}
       
        # read_only_fields = ['user']
# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=4000)
#     post_image=serializers.ImageField()
#     author_id = serializers.IntegerField()
#     post_date=serializers.DateField()

#     def create(self, validated_data):
#         return Post.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.author_id = validated_data.get('author_id', instance.author_id)
#         instance.post_image=validated_data.get('post_image', instance.post_image)
#         instance.post_date = validated_data.get('post_date', instance.post_date)
#         instance.save()
#         return instance
    