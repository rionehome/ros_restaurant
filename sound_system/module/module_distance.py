import os

from . import module_pico
from . import module_beep

import datetime

file_path = os.path.abspath(__file__)

# Define path
result_path = file_path.replace(
    'module/module_distance.py', 'log/distance-{}.txt').format(str(datetime.datetime.now()))

def beep(number):
    ###############
    #
    # use this module to detect right or left
    #
    # param >> number: right|left
    #
    # return >> None
    #
    ###############

    number = number.split("|")
    place = ""
    if number[0] > number[1]:place="right"
    else:place="left"
    right_or_left = "I'm at " + place +" side, because " \
                    "distance from right wall is {} meters" \
                    " but distance from left wall is {} meters.".format(number[0], number[1])
    module_beep.beep("stop")
    print("\n-----------------------------")
    print(right_or_left)
    print("-----------------------------\n")
    module_pico.speak(right_or_left)
    file = open(result_path, 'a')
    file.write(str(datetime.datetime.now()) + ": " + str(right_or_left) + "\n")
    file.close()

    return 1


if __name__ == '__main__':
    beep("15.3|2.5")

