
class AMCMovie:
    def __init__(self, name, actors, director, genre, rating):
        self.name = name
        self.actor_list = actors
        self.director = director
        self.genre = genre
        self.rating = rating

    def print_self(self):
        print('Name: {}. Actors: {}'.format(self.name, self.actor_list.title()))


class AMCLocation:
    def __init__(self, name, id, website, phone_num, street_address, city, state, zip_code):
        self.name = name
        self.id = id
        self.website = website
        self.phone_num = phone_num
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def print_self(self):
        print('Name: {}. Address: {}, {} {} {}'.format(self.name, self.street_address, self.city.title(), self.state, self.zip_code))
