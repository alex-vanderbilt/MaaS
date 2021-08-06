from twilio.rest import Client
from Notifications.twilio_config import twilio_account_sid, twilio_auth_token, twilio_verification_service


class TextNotification:
    def __init__(self):
        self.client = Client(twilio_account_sid, twilio_auth_token)
        self.from_ = '+16152056943'
        self.body = None

    def buildMessageBody(self, amc_showing, amc_location):
        # This is a test text and a rough outline of how I think things should look. This is dynamically generated with
        # our code (and the link at the bottom works!)
        self.body = 'Movie Suggestion:\n' \
                    '{} is playing at {} at {}.\n\n' \
                    'Purchase tickets here: {}'\
                    .format(amc_showing.name, amc_location.name, amc_showing.show_time_local, amc_showing.purchase_url)

    '''dest_phone_number: the phone number we are sending our text to, in the following format: +XXXXXXXXXXX
    '''
    def sendText(self, dest_phone_number):
        print('Sending the following text: {}'.format(self.body))
        self.client.messages.create(body=self.body,
                                    from_=self.from_,
                                    to=dest_phone_number
                                    )

    def init_verification(self, dest_phone_number):
        verification = self.client.verify \
            .services(twilio_verification_service) \
            .verifications \
            .create(to=dest_phone_number, channel='sms')

        return verification.sid

    def confirm_verification(self, dest_phone_number, verification_code):
        verification_check = self.client.verify \
            .services(twilio_verification_service) \
            .verification_checks \
            .create(to=dest_phone_number, code=verification_code)

        # print(verification_check.status)
        if verification_check.status == "approved":
            return True
        else:
            return False
