from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest
from Notifications.notification_service import TextNotification

requester = AMCRequest()
notifier = TextNotification()

# current_movie_list = requester.get_current_movies()
# print("Current playing movies at AMC:")
# for movie in current_movie_list:
#     movie.print_self()
#
# theater_list = requester.get_locations_via_zip('90210')
# print("\nTheater locations:")
# for theater in theater_list:
#     theater.print_self()

# pretty_json = json.loads(response.text)
# print(json.dumps(pretty_json, indent=2))

theater_id = 6215

theater = requester.get_theater_via_id(theater_id)
print('Theater {} has the following movies playing:\n'.format(theater.name))

showtime_list = requester.get_showtimes_via_id(theater_id)
for showtime in showtime_list:
    print('{} is playing at {} in auditorium {}'.format(showtime.name, showtime.show_time_local, showtime.auditorium))

notifier.buildMessageBody(showtime_list[0], theater)
notifier.sendText('+19169904213')