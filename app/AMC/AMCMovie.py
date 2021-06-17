
class AMCMovie:
    def __init__(self, name, actors, director, genre, rating):
        self.name = name
        self.actor_list = actors
        self.director = director
        self.genre = genre
        self.rating = rating

    def print_self(self):
        print('Name: {}. Actors: {}'.format(self.name, self.actor_list))
