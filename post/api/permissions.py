from rest_framework import permissions

class OwnerOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission class which allow
    object owner to do all http methods"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author.id == request.user.id


class IsOwnerOrPostOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission class which allow comment owner to do all http methods
    and Post Owner to DELETE comment"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE' and \
                obj.post.author.id == request.user.id:
            return True

        return obj.author.id == request.user.id

# class IsPostOrCommentOwner(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method == "DELETE": 
#             # check here if the user is owner of the post or comment
#             return obj.owner == request.user or obj.post.author == request.user

#         # else always return True.
#         return True