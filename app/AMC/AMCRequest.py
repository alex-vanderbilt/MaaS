import requests
from requests.exceptions import HTTPError
from AMC.config import api_secret
from AMC.AMC import AMCMovie, AMCLocation, AMCShowing
import json

class AMCRequest:
    def __init__(self):
        self.api_endpoint = "https://api.amctheatres.com"
        self.query_url = None
        self.requests = None
        self.page_size = 10
        self.header = {
            'content-type': 'text',
            'x-amc-vendor-key': api_secret
        }

    def request_data(self):
        response = requests.get(self.api_endpoint + self.query_url, headers=self.header)
        # pretty_json = json.loads(response.text)
        # print(json.dumps(pretty_json, indent=2))
        try:
            response.raise_for_status()
        except HTTPError:
            print('Error from HTTP response')
            print(response)
        return response

    def get_current_movies(self):
        self.query_url = '/v2/movies/views/now-playing?page-size={}'.format(self.page_size)
        response = self.request_data()
        movie_list = []
        for movie in response.json()["_embedded"]["movies"]:
            name = movie['name']
            actors = movie['starringActors']
            director = movie['directors']
            genre = movie['genre']
            rating = movie['mpaaRating']
            movie_list.append(AMCMovie(name=name, actors=actors.title(), director=director, genre=genre.title(), rating=rating))
        return movie_list

    def get_theater_via_id(self, theater_id):
        self.query_url = '/v2/theatres/{}'.format(theater_id)
        response = self.request_data()
        # TODO - handle 404 when theater is not found (bad theater_id)
        name = response.json()['name']
        id = response.json()['id']
        phone_num = response.json()['guestServicesPhoneNumber']
        website = response.json()['websiteUrl']
        street_address = response.json()['location']['addressLine1']
        city = response.json()['location']['city'].title()
        zip_code = response.json()['location']['postalCode']
        state = response.json()['location']['state']
        return AMCLocation(name=name, id=id, website=website, phone_num=phone_num,
                    street_address=street_address, city=city, state=state, zip_code=zip_code)

    def get_showtimes_via_id(self, theater_id):
        self.query_url = '/v2/theatres/{}/showtimes'.format(theater_id)
        response = self.request_data()
        showtime_list = []
        for showtimes in response.json()["_embedded"]["showtimes"]:
            movie_id = showtimes['movieId']
            name = showtimes['movieName']
            genre = showtimes['genre'].title()
            show_time_local = showtimes['showDateTimeLocal']
            theater_id = showtimes['theatreId']
            auditorium = showtimes['auditorium']
            rating = showtimes['mpaaRating']
            purchase_url = showtimes['purchaseUrl']
            movie_url = showtimes['movieUrl']
            ticket_price_adult = showtimes['ticketPrices'][0]['price']
            showtime_list.append(AMCShowing(movie_id, name, genre, show_time_local, theater_id, auditorium, rating, purchase_url, movie_url, ticket_price_adult))
        return showtime_list

    def get_locations_via_zip(self, zip_code):
        self.query_url = '/v2/location-suggestions/?query={}'.format(zip_code)
        zip_code_response = self.request_data()
        # This may break if we get multiple suggestions for lat/long searches. Not sure if that will ever happen
        lat_long_url = zip_code_response.json()["_embedded"]["suggestions"][0]["_links"]['https://api.amctheatres.com/rels/v2/locations']['href']
        self.query_url = lat_long_url.split(self.api_endpoint)[1] # results in something like /v2/locations?latitude=39.679437&longitude=-104.96473
        lat_lon_response = self.request_data()
        theater_list = []
        for theater in lat_lon_response.json()["_embedded"]["locations"]:
            name = theater['_embedded']['theatre']['name']
            id = theater['_embedded']['theatre']['id']
            phone_num = theater['_embedded']['theatre']['guestServicesPhoneNumber']
            website = theater['_embedded']['theatre']['websiteUrl']
            street_address = theater['_embedded']['theatre']['location']['addressLine1']
            city = theater['_embedded']['theatre']['location']['city'].title()
            zip_code = theater['_embedded']['theatre']['location']['postalCode']
            state = theater['_embedded']['theatre']['location']['state']
            theater_list.append(AMCLocation(name=name, id=id, website=website, phone_num=phone_num,
                                            street_address=street_address, city=city, state=state, zip_code=zip_code))
        return theater_list



