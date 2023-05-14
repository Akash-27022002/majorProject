from rest_framework import serializers
from predicition.models import *

class PredicitionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Predictions
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    history = PredicitionSerializer(many = True)
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields =("name","email","password")
    def validate_password(self, password):
        if password:
            if len(password) < 4:
                raise serializers.ValidationError(
                    "Password must be at least 4 characters long!"
                )
        return password