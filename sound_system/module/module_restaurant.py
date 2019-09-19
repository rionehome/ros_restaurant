import os
from pocketsphinx import LiveSpeech, get_model_path

from .import module_speak

import datetime
from time import sleep

noise_words = []
file_path = os.path.abspath(__file__)

# pocketsphinx path
model_path = get_model_path()

# Define order path
order_dic_path = file_path.replace(
    'module/module_restaurant.py', 'dictionary/restaurant.dict')
order_gram_path = file_path.replace(
    'module/module_restaurant.py', 'dictionary/restaurant.gram')

# Define yes or no path
yes_no_dic_path = file_path.replace(
    'module/module_restaurant.py', 'dictionary/yes_no.dict')
yes_no_gram_path = file_path.replace(
    'module/module_restaurant.py', 'dictionary/yes_no.gram')

# log file
result_path = file_path.replace(
    'module/module_restaurant.py', 'log/restaurant-{}.txt').format(str(datetime.datetime.now()))

food = None

# Listen question, or speak the number of men and women
def restaurant(when):

    ###############
    #
    # use this module at restaurant section
    #
    # param >> (first or end): when will you use at restaurant section
    #
    # return >> restart: if ducker mistakes custamer, return is this to go back to the first position
    #           str(food): if  ducker takes order, return is food's name
    #
    ###############

    global noise_words
    global live_speech
    global food
    if when == "first":
            start_sentence = "Do you want me to take orders ?"
            print("\n---------------------------------\n",start_sentence,"\n---------------------------------\n")
            module_speak.speak(start_sentence)

            # Detect yes or no
            setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-20)
            sleep(1)
            for question0 in live_speech:
                print("\n[*] CONFIRMING ...")
                #print(question0)

                # Noise list
                noise_words = read_noise_word(yes_no_gram_path)

                if str(question0) not in noise_words:
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now())+": "+str(question0)+"\n")
                    file.close()
                    if str(question0) == "yes":

                        # Deside order
                        answer = "Sure, please order me."
                        print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                        pause()
                        module_speak.speak(answer)
                        break

                    elif str(question0) == "no":

                        # Fail, Ask yes-no question
                        answer = "Sorry."
                        print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                        pause()
                        module_speak.speak(answer)
                        return "restart"

                    elif str(question0) == "please say again":

                        print("\n---------------------------------\n",start_sentence,"\n---------------------------------\n")
                        pause()
                        module_speak.speak(start_sentence)

                        # Ask yes-no question
                        setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-20)

                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] CONFIRMING ...")
                    pass


            setup_live_speech(False, order_dic_path, order_gram_path, 1e-10)
            sleep(1)
            for question1 in live_speech:
                #sleep(1)
                print("\n[*] PREASE ORDER ...")
                #print(question1)

                # Noise list
                noise_words = read_noise_word(order_gram_path)
                if str(question1) == "":
                    pass
                elif str(question1) not in noise_words:
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now())+": "+str(question1)+"\n")
                    file.close()
                    print("\n-----------your order-----------\n",str(question1),"\n---------------------------------\n")
                    food = str(question1).replace("I want ","")
                    sentence = "Do you want " + str(food) + " ?"
                    print("\n---------------------------------\n",sentence,"\n---------------------------------\n")

                    # Ask yes-no question
                    pause()
                    module_speak.speak(sentence)

                    # Detect yes or no
                    setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)
                    flag = True
                    while flag:
                        for question2 in live_speech:
                            print("\n[*] CONFIRM YOUR OREDER ...")
                            #print(question2)

                            # Noise list
                            noise_words = read_noise_word(yes_no_gram_path)

                            if str(question2) not in noise_words:
                                file = open(result_path, 'a')
                                file.write(str(datetime.datetime.now())+": "+str(question2)+"\n")
                                file.close()

                                if str(question2) == "yes":

                                    # Deside order
                                    answer = "Sure, I will bring " + str(food) + "."
                                    print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                                    pause()
                                    module_speak.speak(answer)
                                    return str(food)

                                elif str(question2) == "no":

                                    # Fail, oreder one more time
                                    answer = "Sorry, prease order one more."
                                    print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                                    pause()
                                    module_speak.speak(answer)
                                    setup_live_speech(False, order_dic_path, order_gram_path, 1e-10)
                                    flag = False
                                    break


                                elif str(question2) == "please say again":

                                    pause()
                                    print("\n---------------------------------\n",sentence,"\n---------------------------------\n")
                                    module_speak.speak(sentence)

                                    # Ask yes-no question to barman
                                    setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-10)

                            # noise
                            else:
                                print(".*._noise_.*.")
                                print("\n[*] CONFIRM YOUR OREDER ...")
                                pass

                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] PREASE ORDER ...")
                    pass

    elif when == "end":
        # Detect yes or no
        while True:
            setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-20)
            end_sentence = "Did you take items ?"
            print("\n---------------------------------\n",end_sentence,"\n---------------------------------\n")
            module_speak.speak(end_sentence)
            for question3 in live_speech:
                print("\n[*] CONFIRM OREDER ...")
                #print(question3)

                # Noise list
                noise_words = read_noise_word(yes_no_gram_path)

                if str(question3) not in noise_words:
                    file = open(result_path, 'a')
                    file.write(str(datetime.datetime.now())+": "+str(question3)+"\n")
                    file.close()
                    if str(question3) == "yes":

                        # Deside order
                        answer = "Thank you."
                        print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                        pause()
                        module_speak.speak(answer)
                        return 1

                    elif str(question3) == "no":

                        # Fail, Ask yes-no question
                        answer = "Sorry, please take this item."
                        print("\n---------------------------------\n",answer,"\n---------------------------------\n")
                        pause()
                        module_speak.speak(answer)

                        # Ask yes-no question
                        print("\n---------------------------------\n",end_sentence,"\n---------------------------------\n")
                        module_speak.speak(end_sentence)
                        setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-20)


                    elif str(question3) == "please say again":

                        # Ask yes-no question
                        print("\n---------------------------------\n",end_sentence,"\n---------------------------------\n")
                        pause()
                        del(live_speech)
                        module_speak.speak(end_sentence)
                        setup_live_speech(False, yes_no_dic_path, yes_no_gram_path, 1e-20)

                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] CONFIRM OREDER ...")
                    pass


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


# Make noise list
def read_noise_word(gram_path):

    ###############
    #
    # use this module to put noise to list
    #
    # param >> gram_path: grammer's path which you want to read noises
    #
    # return >> words: list in noises
    #
    ###############

    words = []
    with open(gram_path) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace(
                    " = ", "").replace("\n", "").replace(";", "")
            words = line.split(" | ")
    return words

# Setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):

    ###############
    #
    # use this module to set live espeech parameter
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

if __name__ == '__main__':
    last_order = restaurant("first")
    if str(last_order) != "restart" and last_order != 1:
        print("Simulation: Going back to the first position ...")
        sleep(3)
        last_sentence = "order is "+last_order+", please put "+last_order+" on me, thank you."

        print(last_sentence)
        module_speak.speak(last_sentence)
