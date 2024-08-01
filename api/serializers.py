from rest_framework import serializers 
from image_generator.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email', 'original_photo','prompted_photo']


         