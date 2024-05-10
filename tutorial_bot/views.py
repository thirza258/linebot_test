from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import linebot.v3.messaging
from linebot.v3.messaging.models.push_message_request import PushMessageRequest
from linebot.v3.messaging.models.push_message_response import PushMessageResponse
from linebot.v3.messaging.rest import ApiException
from pprint import pprint
import os

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


# Defining the host is optional and defaults to https://api.line.me
# See configuration.py for a list of all supported configuration parameters.
configuration = linebot.v3.messaging.Configuration(
    host = "https://api.line.me"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: Bearer
configuration = linebot.v3.messaging.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with linebot.v3.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linebot.v3.messaging.MessagingApi(api_client)
    push_message_request = linebot.v3.messaging.PushMessageRequest() # PushMessageRequest | 
    x_line_retry_key = '' # str | Retry key. Specifies the UUID in hexadecimal format (e.g., `123e4567-e89b-12d3-a456-426614174000`) generated by any method. The retry key isn't generated by LINE. Each developer must generate their own retry key.  (optional)

    try:
        api_response = api_instance.push_message(push_message_request, x_line_retry_key=x_line_retry_key)
        print("The response of MessagingApi->push_message:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->push_message: %s\n" % e)
        
# Enter a context with an instance of the API client
with linebot.v3.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = linebot.v3.messaging.MessagingApi(api_client)
    broadcast_request = linebot.v3.messaging.BroadcastRequest() # BroadcastRequest | 
    x_line_retry_key = 'x_line_retry_key_example' # str | Retry key. Specifies the UUID in hexadecimal format (e.g., `123e4567-e89b-12d3-a456-426614174000`) generated by any method. The retry key isn't generated by LINE. Each developer must generate their own retry key.  (optional)

    try:
        api_response = api_instance.broadcast(broadcast_request, x_line_retry_key=x_line_retry_key)
        print("The response of MessagingApi->broadcast:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->broadcast: %s\n" % e)