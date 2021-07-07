import schedule
import time
from datetime import datetime

def test():
    current_time = datetime.now().strftime("%H:%M:%S")
    print('Test printed at: ' + current_time)

print('Starting')
test()
schedule.every(10).minutes.do(test)

while True:
    schedule.run_pending()
    time.sleep(1)