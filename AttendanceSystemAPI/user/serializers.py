from rest_framework import serializers
# database
from .models import User
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = '__all__'
      
   def create(self, validated_data):
      user = User(
         username=validated_data['username'],
         password=validated_data['password']
      )
      user.set_password(validated_data['password'])
      user.save()
      return user