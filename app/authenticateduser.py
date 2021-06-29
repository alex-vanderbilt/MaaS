class AuthenticatedUser:
    def __init__(self):
        self.username = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.pcm = None
        self.fmg = None
        self.secret_key = None
        self.verified = "False"

    def update_user(self, username, email, first_name, last_name, phone_number, pcm, fmg, sk):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.pcm = pcm
        self.fmg = fmg
        self.secret_key = sk
        self.verified = "True"

    def log_out_user(self):
        self.username = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.pcm = None
        self.fmg = None
        self.secret_key = None
        self.verified = "False"


authenticated_user = AuthenticatedUser()
