from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TextMessageUser
from tutorial_bot.views import handle_message, push_message
from .serializers import TextMessageUserSerializer



# Create your views here.
class TextMessageUserViews(APIView):
    def get(self, request):
        try:
            text_message_user = TextMessageUser.objects.all()
            serializer = TextMessageUserSerializer(text_message_user, many=True)
            return Response({"text_message_user": serializer.data}, status=status.HTTP_200_OK)
        except TextMessageUser.DoesNotExist:
            return Response({"error": "TextMessageUser not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        try:
            user_id = request.data["user_id"]
            text_message = request.data["text_message"]
            text_message_user = TextMessageUser.objects.create(user_id=user_id, text_message=text_message)
            push_message()
            text_message_user.save()
            return Response({"text_message_user": "created"}, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)