from rest_framework import serializers
from .models import TextMessageUser

class TextMessageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessageUser
        fields = "__all__"