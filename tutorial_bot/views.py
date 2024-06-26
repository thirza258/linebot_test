from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import linebot.v3.messaging
# from linebot.v3.messaging.models.push_message_request import PushMessageRequest
# from linebot.v3.messaging.models.push_message_response import PushMessageResponse
# from linebot.v3.messaging.rest import ApiException
from pprint import pprint
import os
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    LocationMessageContent,
    StickerMessageContent,
    ImageMessageContent,
    VideoMessageContent,
    AudioMessageContent,
    FileMessageContent,
    UserSource,
    RoomSource,
    GroupSource,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    LeaveEvent,
    PostbackEvent,
    BeaconEvent,
    MemberJoinedEvent,
    MemberLeftEvent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    PushMessageRequest,
    MulticastRequest,
    BroadcastRequest,
    TextMessage,
    ApiException,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    TemplateMessage,
    FlexMessage,
    Emoji,
    QuickReply,
    QuickReplyItem,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    FlexBubble,
    FlexImage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    ErrorResponse
)

from linebot.v3.insight import (
    ApiClient as InsightClient,
    Insight
)

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
    user_msg = event.message.text

    if "reply" in user_msg:
        response = user_msg
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    elif "coba" in user_msg:
        response = user_msg
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Coba " + response)
        )
    elif "saya" in user_msg:
        # response = event.source.user_id
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text="Anda " + response)
        # )
        if event.source.type == "user":
            response = f"Anda adalah {event.source.user_id}"
        elif event.source.type == "group":
            response = f"Group ID Anda adalah {event.source.group_id}"
        elif event.source.type == "room":
            response = f"Room ID Anda adalah {event.source.room_id}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    else:
        response = "Maaf, saya tidak mengerti pesan Anda"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

# @csrf_exempt
# @handler.default()
def push_message():
    list_push = ["Ude96a2cc59965c6086cf4b280af2655d", "Ce6606c634ff160397a13267e3d4458fa"]

    try:
        for i in list_push:
            line_bot_api.push_message(
                to= i,
                messages=[TextSendMessage(text="Hello, world!")]
            )
        # line_bot_api.push_message(
        #     # PushMessageRequest(
        #         to= "Ce6606c634ff160397a13267e3d4458fa",
        #         messages=[TextSendMessage(text="Hello, world!")]
        #     # )
        # )
        
    except LineBotApiError as e:
        print(e)

# Defining the host is optional and defaults to https://api.line.me
# See configuration.py for a list of all supported configuration parameters.


# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: Bearer
# configuration = linebot.v3.messaging.Configuration(
#     access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
# )

# # Enter a context with an instance of the API client
# with linebot.v3.messaging.ApiClient(configuration) as api_client:
#     # Create an instance of the API class
#     api_instance = linebot.v3.messaging.MessagingApi(api_client)
#     push_message_request = linebot.v3.messaging.PushMessageRequest() # PushMessageRequest | 
#     x_line_retry_key = '' # str | Retry key. Specifies the UUID in hexadecimal format (e.g., `123e4567-e89b-12d3-a456-426614174000`) generated by any method. The retry key isn't generated by LINE. Each developer must generate their own retry key.  (optional)

#     try:
#         api_response = api_instance.push_message(push_message_request, x_line_retry_key=x_line_retry_key)
#         print("The response of MessagingApi->push_message:\n")
#         pprint(api_response)
#     except Exception as e:
#         print("Exception when calling MessagingApi->push_message: %s\n" % e)
        
# # Enter a context with an instance of the API client
# with linebot.v3.messaging.ApiClient(configuration) as api_client:
#     # Create an instance of the API class
#     api_instance = linebot.v3.messaging.MessagingApi(api_client)
#     broadcast_request = linebot.v3.messaging.BroadcastRequest() # BroadcastRequest | 
#     x_line_retry_key = 'x_line_retry_key_example' # str | Retry key. Specifies the UUID in hexadecimal format (e.g., `123e4567-e89b-12d3-a456-426614174000`) generated by any method. The retry key isn't generated by LINE. Each developer must generate their own retry key.  (optional)

#     try:
#         api_response = api_instance.broadcast(broadcast_request, x_line_retry_key=x_line_retry_key)
#         print("The response of MessagingApi->broadcast:\n")
#         pprint(api_response)
#     except Exception as e:
#         print("Exception when calling MessagingApi->broadcast: %s\n" % e)