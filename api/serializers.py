from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ValidateMailFormSerializer(serializers.Serializer):
    remote_id = serializers.CharField(required=True,max_length=25)
    email_to = serializers.CharField(required=True,max_length=50)
    subject = serializers.CharField(required=True,max_length=100)
    message = serializers.CharField(required=True)
    language = serializers.CharField(required=True,max_length=25)