from twilio.rest import Client
from twilio_config import twilio_account_sid, twilio_auth_token

client = Client(twilio_account_sid, twilio_auth_token)

message = client.messages.create(
                     body="Hello world",
                     from_='+16152056943',
                     to='+19169904213'
                 )

print(message.sid)