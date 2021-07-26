class AuthenticatedUser:
    def __init__(self):
        self.username = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.zipcode = None
        self.pcm = None
        self.fmg = None
        self.secret_key = None
        self.favorited_theaters = []
        self.last_searched_zipcode = None
        self.verified = "False"
        self.authenticated = "False"
        self.favorite_theater = "None"
        self.favorite_theater_name = "None"
        self.theater_string = "None"
        self.preferred_time = "None"
        self.preferred_day = "None"

    def update_user(self, username, email, first_name, last_name, phone_number, zipcode, pcm, fmg, sk):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.zipcode = zipcode
        self.pcm = pcm
        self.fmg = fmg
        self.secret_key = sk
        self.verified = "True"

    def set_favorited_theater(self, favorite):
        if self.favorite_theater is favorite:
            self.favorite_theater = "None"
            self.theater_string = "None"
        else:
            self.favorite_theater = favorite

    def set_theater_information(self, info):
        self.theater_string = info

    def set_day_of_week(self, day):
        self.preferred_day = day

    def set_time_of_day(self, time):
        self.preferred_time = time

    def log_out_user(self):
        self.username = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.zipcode = None
        self.pcm = None
        self.fmg = None
        self.secret_key = None
        self.favorited_theaters = []
        self.last_searched_zipcode = None
        self.verified = "False"
        self.authenticated = "False"
        self.favorite_theater = "None"
        self.theater_string = "None"

    def user_authenticated(self):
        self.authenticated = "True"

    def update_last_zipcode(self, zipcode):
        self.last_searched_zipcode = zipcode

    def add_favorited_theater(self, theater_id):
        self.favorited_theaters.append(theater_id)


authenticated_user = AuthenticatedUser()
