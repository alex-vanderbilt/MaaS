from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest

requester = AMCRequest()

current_movie_list = requester.get_current_movies()
print("Current playing movies at AMC:")
for movie in current_movie_list:
    movie.print_self()

theater_list = requester.get_locations_via_zip('90210')
print("\nTheater locations:")
for theater in theater_list:
    theater.print_self()

# pretty_json = json.loads(response.text)
# print(json.dumps(pretty_json, indent=2))