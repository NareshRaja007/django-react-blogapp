from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = UserDetails
        fields = ['user_id', 'name', 'contact_number', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = UserDetails.objects.filter(user_id=data['user_id']).first()
        if user and check_password(data['password'], user.password):
            tokens = RefreshToken.for_user(user)
            return {
                'refresh': str(tokens),
                'access': str(tokens.access_token),
                'user': {
                    'id': user.user_id,
                    'name': user.name,
                    'contact_number': user.contact_number,
                }
            }
        raise serializers.ValidationError("Invalid credentials")
    

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'user', 'title', 'content', 'created_at', 'created_by', 'updated_at']
        extra_kwargs = {'user': {'read_only': True}, 'created_by': {'read_only': True}}
