from rest_framework.exceptions import NotAuthenticated, PermissionDenied

def check_object_permission(self, obj):
   user = self.request.user
   if user.role.name != "admin" and obj.id != user.id:
      raise PermissionDenied("You are not allowed to modify other users' information!")

   def update(self, request, *args, **kwargs):
      instance = self.get_object()
      self.check_object_permission(instance)
      return super().update(request, *args, **kwargs)

   def partial_update(self, request, *args, **kwargs):
      instance = self.get_object()
      self.check_object_permission(instance)
      return super().partial_update(request, *args, **kwargs)

   def destroy(self, request, *args, **kwargs):
      instance = self.get_object()
      self.check_object_permission(instance)
      return super().destroy(request, *args, **kwargs)
   
def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        current_user = request.user if request else None

        if current_user and hasattr(current_user, 'role'):
            if current_user.role and current_user.role.name in ["teacher", "admin"]:
                rep.pop("classes", None)

        return rep