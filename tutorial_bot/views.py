from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

def index(request):
    return HttpResponse("Hello, World!")

@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        global domain
        domain = request.META['HTTP_HOST']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body=body, signature=signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        return HttpResponse()
    else :
        return HttpResponseBadRequest()
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
        
