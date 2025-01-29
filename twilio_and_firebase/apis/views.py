from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .models import TwilioCredentials
from .serializers import TwilioCredentialsSerializer
from django.conf import settings
from twilio_and_firebase.settings import env

""" view for sending a message """
# def send_message(request):
#     account_sid = env("TWILIO_ACCOUNT_SID")
#     auth_token = env("TWILIO_AUTH_TOKEN")
#     my_number = env("TWILIO_PHONE_NUMBER")
    
#     client = Client(account_sid, auth_token)
    
#     message_body = "Join Earth's mightiest heroes. Like Kevin Bacon."
    
#     message = client.messages.create(
#         body = message_body,
#         from_= my_number,
#         to="+923164477192",
#     )
    
#     context = {
#         'from_number': my_number,
#         'to_number': message.to,
#         'body': message.body,
#     }
    
#     return render(request, 'message_details.html', context)

""" view for making a call """
# def make_call(request):
#     account_sid = env("TWILIO_ACCOUNT_SID")
#     auth_token = env("TWILIO_AUTH_TOKEN")
#     my_number = env("TWILIO_PHONE_NUMBER")
    
#     client = Client(account_sid, auth_token)
    
#     try:
#         call = client.calls.create(
#             to="+923164477192",  # The phone number you want to call
#             from_=my_number,     # Your Twilio phone number
#             url="http://demo.twilio.com/docs/voice.xml"  # TwiML URL
#         )
        
#         context = {
#             'call_sid': call.sid,
#             'from_number': my_number,
#             'to_number': call.to,
#             'status': call.status,
#         }
        
#         return render(request, 'call_details.html', context)
    
#     except TwilioRestException as e:
#         error_message = str(e)
#         return render(request, 'error.html', {'error_message': error_message})


class TwilioClient:
    @staticmethod
    def get_client(user=None):
        if user and user.is_authenticated:
            # Try to get the user's Twilio credentials
            credentials = user.twilio_credentials
            if credentials and all([credentials.account_sid, credentials.auth_token, credentials.phone_number]):
                account_sid = credentials.account_sid
                auth_token = credentials.auth_token
                phone_number = credentials.phone_number
            else:
                # Fall back to default credentials
                account_sid = env("TWILIO_ACCOUNT_SID")
                auth_token = env("TWILIO_AUTH_TOKEN")
                phone_number = env("TWILIO_PHONE_NUMBER")
        else:
            # Fallback to default credentials if user is not authenticated
            account_sid = env("TWILIO_ACCOUNT_SID")
            auth_token = env("TWILIO_AUTH_TOKEN")
            phone_number = env("TWILIO_PHONE_NUMBER")
        
        # return account_sid, auth_token, phone_number ### test
        return Client(account_sid, auth_token), phone_number


@api_view(['POST'])
def send_message(request):
    """
    API to send a message using Twilio
    """
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Get the Twilio client and from number (using user's credentials if available)
        client, from_number = TwilioClient.get_client(request.user)

        # The message body and the recipient's phone number (hardcoded for now)
        to_number = "+923164477192"
        message_body = "This is a test message from Twilio."

        # Send the message using Twilio's API
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        # Return success response with message details
        return Response({
            "message_sid": message.sid,
            "status": message.status,
            "from_number": from_number,
            "to_number": message.to,
            "body": message.body
        }, status=status.HTTP_200_OK)
        
        ############################## test #########################################
        # account_sid, auth_token, phone_number = TwilioClient.get_client(request.user)
        
        # return Response({
        #         'from_number': account_sid,
        #         'to_number': auth_token,
        #         'body': phone_number,
        #     })
        
        ############################## test #########################################
    
    except TwilioRestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def make_call(request):
    """
    API to make a call using Twilio
    """
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Get the Twilio client and from number (using user's credentials if available)
        client, from_number = TwilioClient.get_client(request.user)

        # The recipient's phone number (hardcoded for now)
        to_number = "+923164477192"
        
        # Make the call
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url="http://demo.twilio.com/docs/voice.xml"
        )

        # Return success response with call details
        return Response({
            "call_sid": call.sid,
            "status": call.status,
            "from_number": from_number,
            "to_number": call.to
        }, status=status.HTTP_200_OK)

    except TwilioRestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
