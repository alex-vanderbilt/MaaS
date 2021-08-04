from AMC.AMC import AMCMovie
from AMC.AMCRequest import AMCRequest
from Notifications.notification_service import TextNotification

# current_movie_list = requester.get_current_movies()
# print("Current playing movies at AMC:")
# for movie in current_movie_list:
#     movie.print_self()

requester = AMCRequest()
notifier = TextNotification()

# zip_code = '90210'
#
# theater_list = requester.get_locations_via_zip(zip_code)
# print("Theater locations near {}:\n".format(zip_code))
# for theater in theater_list:
#     theater.print_self()
#
# if theater_list[0] != None:
#     theater_id = theater_list[0].id
# else:
#     theater_id = 2416
#
# theater = requester.get_theater_via_id(theater_id)
# print('\nTheater {} has the following movies playing:\n'.format(theater.name))
#
# showtime_list = requester.get_showtimes_via_id(theater_id)
# for showtime in showtime_list:
#     print('{} is playing at {} in auditorium {}\n'.format(showtime.name, showtime.show_time_local, showtime.auditorium))

# notifier.buildMessageBody(showtime_list[0], theater)
# notifier.sendText('+19169904213')

notifier.verifyPhone('+19169904213')