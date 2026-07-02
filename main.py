import time

from detector import in_meeting
from recorder import start, stop

recording = False

while True:

    meeting = in_meeting()

    if meeting and not recording:

        print("開始錄影")

        start()

        recording = True

    elif not meeting and recording:

        print("停止錄影")

        stop()

        recording = False

    time.sleep(2)