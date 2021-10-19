from rest_framework import serializers
from .models import User
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password


#class UserCodeSendSerializer(serializers.Serializer):
#    phone_number = serializers.CharField(required=True)



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    password2 = serializers.CharField(write_only=True, label='Confirm password',required=True)
    class Meta:
        fields = ['full_name','phone_number',  'password', 'password2']
        model = User
    def validate_password(self, password):
        if password != self.initial_data['password2']:
            raise serializers.ValidationError('Passwords do not match!')    
        return password   
    
    def create(self,validated_data):
        full_name = validated_data['full_name']
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        user = User(full_name=full_name, phone_number=phone_number)
        user.set_password(password=password)
        user.save()
        return user
        
class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32)
    phone_regex = RegexValidator(
        regex=r'^\d{9}$', message="901234567 holatda kiriting")
    phone_number = serializers.CharField(required=True, validators=[phone_regex])


class UserProfileSerializer(serializers.Serializer):
    models = User
    fields = ['full_name', 'phone_number','date_joined']
    read_only_fields = ('phone_number')

    