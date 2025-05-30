from rest_framework import serializers, response
from django.contrib.auth import get_user_model
from roles.models import Role
from roles.serializer import RoleSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True, required=False)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=False,
        write_only=True,
        allow_null=True,
        source='role'
    )
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'phone_number', 'address', 'date_of_birth', 'avatar', 'role', 'role_id']
        
    # def update(self, instance, validated_data):
    #     request = self.context.get("request")
    #     user = request.user if request else None

    #     if user and user.role and user.role.name == "admin":
    #         role = validated_data.get("role", None)
    #         is_active = validated_data.get("is_active", None)
    #         validated_data.clear()
    #         if role is not None:
    #             validated_data["role"] = role
    #         if is_active is not None:
    #             validated_data["is_active"] = is_active
    #     else:
    #         validated_data.pop("role", None)
    #         validated_data.pop("is_active", None)

    #     return super().update(instance, validated_data)

    
class UserInfoSerializer(serializers.ModelSerializer):
    required_alternate_scopes = {
      "list": [["admin"], ["teacher"]],
      "retrieve": [["admin"], ["teacher"]],
      "update": [["admin"], ["teacher"]],
      "destroy": [["admin"]]
    }
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'phone_number', 'address', 'date_of_birth', 'avatar', 'role']
