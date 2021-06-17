import config
import requests
from requests.exceptions import HTTPError
import json
from AMC.AMCMovie import AMCMovie

# importing the api key
api_secret = config.api_secret

# AMCs API endpoint
amc_api = "https://api.amctheatres.com"

# The api_secret is required to be included in the request headers
request_headers = {
    'content-type': 'text',
    'x-amc-vendor-key': api_secret
    }

request_url = amc_api + '/v2/movies/views/now-playing'

# Sending the GET request to the URL with our headers
response = requests.get(request_url, headers=request_headers)

# Ensuring that we received a 200 response code (not a 400,403,404, etc)
try:
    response.raise_for_status()
except HTTPError:
    print('Error from HTTP response')
    print(response)


# pretty_json = json.loads(response.text)
# print(json.dumps(pretty_json, indent=2))

movie_list = []
movie_object_list = []
for movie_info in response.json()["_embedded"]["movies"]:
    # movie_list.append([movie_info['name']])
    name = movie_info['name']
    actors = movie_info['starringActors']
    director = movie_info['directors']
    genre = movie_info['genre']
    rating = movie_info['mpaaRating']
    movie_object_list.append(AMCMovie(name=name, actors=actors, director=director, genre=genre, rating=rating))

print("Current playing movies at AMC:")
for movie in movie_object_list:
    movie.print_self()