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
        fields = '__all__'
        # exclude = ['face_encodings', 'is_superuser', 'is_staff', 'created_at', 'updated_at']

    
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
class UserInfoShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'fullname']
