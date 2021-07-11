
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
        print('Name: {}\nAddress: {}, {} {} {}\nTheater_id: {}\n'.format(self.name, self.street_address, self.city, self.state, self.zip_code, self.id))


class AMCShowing:
    def __init__(self, movie_id, name, genre, show_time_local, theater_id, auditorium, rating, purchase_url, movie_url, ticket_price_adult):
        self.movie_id = movie_id
        self.name = name
        self.genre = genre
        self.show_time_local = show_time_local
        self.theater_id = theater_id
        self.auditorium = auditorium
        self.rating = rating
        self.purchase_url = purchase_url
        self.movie_url = movie_url
        self.ticket_price_adult = ticket_price_adult

