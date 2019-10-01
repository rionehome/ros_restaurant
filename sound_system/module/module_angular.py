import usb
import usb.core
import usb.util
import os
import struct
import csv
import datetime
from pocketsphinx import LiveSpeech, get_model_path

from . import module_pico
from . import module_beep

counter = 0
question_dictionary = {}
noise_words = []
return_list = []
live_speech=None
dev = usb.core.find(idVendor=0x2886,idProduct=0x0018)
file_path = os.path.abspath(__file__)
model_path = get_model_path()

# Define path
dict_path = file_path.replace(
    'module/module_angular.py', 'dictionary/take_the_order.dict')
gram_path = file_path.replace(
    'module/module_angular.py', 'dictionary/take_the_order.gram')
result_path = file_path.replace(
    'module/module_angular.py', 'log/angurar-{}.txt').format(str(datetime.datetime.now()))
# PARAMETERS for sound localization
PARAMETERS = {
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
                       '1 = true (speech detected)')
}

TIMEOUT = 100000

# Find angular
def angular():

    ###############
    #
    # use this module to find angular and detect hotword
    #
    # param >> None
    #
    # return >> angular
    #
    ###############

    global live_speech
    global noise_words
    global return_list
    # Noise list
    noise_words = read_noise_word(gram_path)
    setup_live_speech(False,dict_path,gram_path,1e-10)

    while True:
        if read('SPEECHDETECTED') == 1:
            module_beep.beep("start")
            for phrase in live_speech:
                #print(phrase)
                angular = direction()
                if str(phrase) not in noise_words:
                    if str(phrase) == 'hey ducker take the order':
                        print("angular" + ':' + str(angular), flush=True)
                        pause()
                        module_beep.beep("stop")
                        module_pico.speak("yes sir!")
                        return int(angular)
                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] LISTENING ...")
                    pass

def read_noise_word(gram):

    ###############
    #
    # use this module to put noise to list
    #
    # param >> gram: ~.gram path
    #
    # return >> words: list in noises
    #
    ###############

    words = []
    with open(gram) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace(
                    " = ", "").replace("\n", "").replace(";", "")
            words = line.split(" | ")
    return words

def read(param_name):

    try:
        data = PARAMETERS[param_name]
    except KeyError:
        return

    cmd = 0x80 | data[1]

    if data[2] == 'int':
        cmd |= 0x40

    id = data[0]
    length = 8

    response = dev.ctrl_transfer(
        usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
        0, cmd, id, length, TIMEOUT)

    response = struct.unpack(b'ii', response.tostring())

    if data[2] == 'int':
        result = response[0]
    else:
        result = response[0] * (2. ** response[1])

    return result


def direction():

    ###############
    #
    # use this module to detect angular
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    return read('DOAANGLE')

# Setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):

    ###############
    #
    # use this module to set live speech parameter
    #
    # param >> lm: False >> means useing own dict and gram
    # param >> dict_path: ~.dict file's path
    # param >> jsgf_path: ~.gram file's path
    # param >> kws_threshold: mean's confidence (1e-○)
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)

# Stop lecognition
def pause():

    ###############
    #
    # use this module to stop live speech
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(no_search=True)

if __name__ == '__main__':
    list = angular()
    print(list)
