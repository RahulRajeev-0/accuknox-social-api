# accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

# password validator
from django.contrib.auth.password_validation import validate_password



# User model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')




# Serializer for registeration or signUp
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            try:
                # validating password
                validate_password(password, user=instance)
                instance.set_password(password)
                instance.save()
                return instance
            except serializers.ValidationError as e:
                raise serializers.ValidationError({
                    "password":e.messages
                })

        else:
            raise serializers.ValidationError({
                "password":'Password is not valid'
            })
        
    