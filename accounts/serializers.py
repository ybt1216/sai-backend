from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    nationality = serializers.CharField(write_only=True)
    major = serializers.CharField(write_only=True)
    grade = serializers.IntegerField(write_only=True)
    interests = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True, default='international')
    language = serializers.CharField(write_only=True, default='한국어')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
            'nationality',
            'major',
            'grade',
            'language',
            'interests',
        ]

    def create(self, validated_data):
        role = validated_data.pop('role', 'international')
        nationality = validated_data.pop('nationality')
        major = validated_data.pop('major')
        grade = validated_data.pop('grade')
        language = validated_data.pop('language', '한국어')
        interests = validated_data.pop('interests')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        Profile.objects.create(
            user=user,
            role=role,
            nationality=nationality,
            major=major,
            grade=grade,
            language=language,
            interests=interests,
        )

        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if user is None:
            raise serializers.ValidationError("아이디 또는 비밀번호가 틀렸습니다.")

        data['user'] = user
        return data