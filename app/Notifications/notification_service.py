from twilio.rest import Client
from Notifications.twilio_config import twilio_account_sid, twilio_auth_token
# from AMC.AMC import AMCShowing, AMCLocation

class TextNotification:
    def __init__(self):
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.from_ = '+16152056943'
        self.body = None

    def buildMessageBody(self, amc_showing, amc_location):
        # This is a test text and a rough outline of how I think things should look. This is dynamcially generated with our code (and the link at the bottom works!).\n\n
        self.body = 'Movie Suggestion:\n' \
                    '{} is playing at {} at {}.\n\n' \
                    'Purchase tickets here: {}'.format(amc_showing.name, amc_location.name, amc_showing.show_time_local, amc_showing.purchase_url)

    '''dest_phone_number: the phone number we are sending our text to, in the following format: +XXXXXXXXXXX
    '''
    def sendText(self, dest_phone_number):
        self.client.messages.create(body=self.body,
                                    from_=self.from_,
                                    to=dest_phone_number
                                    )

