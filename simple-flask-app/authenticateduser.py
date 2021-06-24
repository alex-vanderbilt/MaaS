class AuthenticatedUser:
    def __init__(self):
        self.username = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.pcm = None
        self.fmg = None

    def update_user(self, username, email, first_name, last_name, phone_number, pcm, fmg):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.pcm = pcm
        self.fmg = fmg


authenticated_user = AuthenticatedUser()
