from twilio.rest import Client
from twilio_config import twilio_account_sid, twilio_auth_token
from AMC.AMC import AMCShowing

class TextNotification:
    def __init__(self):
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.from_ = '+16152056943'
        self.body = None

    def buildMessageBody(self, AMCShowing):
        self.body = 'Text Body, including showtime information and a link to tickets'
        # TODO - Once AMCShowing has been implemented, create a text template

    '''dest_phone_number: the phone number we are sending our text to, in the following format: +XXXXXXXXXXX
    '''
    def sendText(self, dest_phone_number):
        self.client.messages.create(body=self.body,
                                    from_=self.from_,
                                    to=dest_phone_number
                                    )

