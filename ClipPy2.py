####### IMPORTING #######
from time import sleep
import os
import pyperclip

####### CUSTOM IMPORTS #######
from Notifiers.Audio_nofitier import audio_beep
from Backend.Parser import identify_data, extract_data

Version = "2.1.1.1"
CLR_CMD = 'cls' if os.name == 'nt' else 'clear'


########## GENERAL CLIPBOARD FUNCTION ##########
def get_raw_data_2(b_rem_eol=True, b_rem_return=True, b_rem_d_spacing=True, b_set_lower=False):
    data_raw = pyperclip.paste()

    if b_rem_eol:
        data_raw = data_raw.replace("\n", " ")

    if b_rem_return:
        data_raw = data_raw.replace("\r", " ")

    if b_rem_d_spacing:
        data_raw = data_raw.replace("  ", " ")
        data_raw = data_raw.replace("  ", " ")

    if b_set_lower:
        data_raw = data_raw.lower()

    return data_raw

########## INITIALIZING DATA ##########
def get_cities():
    cities_raw = pyperclip.paste()

    # create a list of data, divided by EoL character
    cities_raw = cities_raw.split("\n")

    # Iterate over raw data to remove Return Character and set to lowercase.
    for idx, data in enumerate(cities_raw):
        cities_raw[idx] = data.replace("\r", "").lower()

    # Original code
    # for idx in range(0, len(data_raw)):
    #     data_raw[idx] = data_raw[idx].replace("\r", "").lower()

    os.system(CLR_CMD)

    print("Cities considered are: ")
    for city in cities_raw:
        print("- ", city)

    return cities_raw


def prompt_option():
    b_flag = True

    while b_flag:
        os.system(CLR_CMD)
        option = input("\nAre these the correct data?<Y/N>:").lower()

        if option == "y":
            b_flag = False
        elif option == "n":
            b_flag = True
        else:
            print("Invalid option: only Y or N")

    return b_flag


def init_city_list():
    b_unfinished = True

    while b_unfinished:
        # os.system(CLR_CMD)

        input("Please copy cities, then press enter")
        cities_list = get_cities()

        b_unfinished = prompt_option()

    os.system(CLR_CMD)

    return cities_list

################################ MAIN LOOP ################################
if __name__ == '__main__':

    """
        STEP 1: Get City list
        User would have to copy all the list of cities from geography.com(Verify?) and paste onto console for parsing
    """
    cities_list = init_city_list()

    # STEP2: Get Raw data to parse
    print("\n-----[Main Program Starting]-----")
    reference = get_raw_data_2()

    while True:
        # Declarations & Reset
        data_raw = ""
        data = ""

        b_is_neither = False
        b_is_what  = "None"

        # Catches:
        #  - Start of program reference
        #  - Last processed copied to clipboard
        if reference == get_raw_data_2():
            sleep(0.5)  # This sleep pauses to avoid instantaneously check currently copied data
            pass
        else:
            try:
                # Step 1: Gets copy of data from clipboard, shows onto display
                data_raw  = get_raw_data_2()
                reference = get_raw_data_2()

                os.system(CLR_CMD)
                print("Data entered -> ", data_raw)

                # Identifies the type of data to parse, skips if invalid data
                data_type = identify_data(data_raw)
                data = extract_data(data, data_type)

                # Audio notifier whether data was valid and classified, or not.
                if data is None:
                    pyperclip.copy(data_raw)
                    audio_beep(freq=200, duration=750)
                    print("Invalid data", "\n")
                else:
                    audio_beep(freq=440, duration=500)
                    print("Copied to clipboard -> ", data)
                    pyperclip.copy(data)
                    reference = data

            except Exception as e:
                print("ERROR", "\n")

#             ############################ MAIN LOOP ################################
# # STEP1 : Get City list
#
# b_unfinished = True
# while b_unfinished:
#     os.system('cls' if os.name == 'nt' else 'clear')
#     cities_list = get_cities()
#     b_unfinished = prompt_option()
#
# os.system('cls' if os.name == 'nt' else 'clear')
# print("\n\nMain Program Starting")
# reference = get_raw_data()
# while True:
#     # Declarations & Reset
#     data_raw = ""
#     data = ""
#
#     b_is_neither = False
#     b_is_what  = "None"
#
#     # Catches:
#     #  - Start of program reference
#     #  - Last processed copied to clipboard
#     if reference == get_raw_data():
#         sleep(0.5)  # This sleep pauses to avoid instantaneously check currently copied data
#         pass
#     else:
#         try:
#             # Step 1: Parse data
#             # Collects data into a list until no more line
#             data_raw = get_raw_data()
#             reference = get_raw_data()
#             data = data_raw.lower()
#
#             # Step 2: Checks for empty data
#             if 1 > len(data):
#                 raise Exception  # Ends this current iteration, and waits for new data
#
#             # Step 3: Clears Display for new data
#             os.system('cls' if os.name == 'nt' else 'clear')
#             print("Data entered -> ", data)
#
#             # Step 4: Check if Email or website
#             b_is_what = parse_link(data)
#
#             # Step 5: Classify data as number or address
#             b_is_what = check_number_address(data) if b_is_what == "None" else b_is_what
#             if b_is_what == "Number":
#                 print(b_is_what)
#                 data = parse_number(data)
#             elif b_is_what == "Address":
#                 print(b_is_what)
#                 data = parse_address_removal(data)
#             elif b_is_what == "Email" or b_is_what == "Web":
#                 print(b_is_what)
#             else:
#                 print("NEITHER")
#                 b_is_neither = True
#
#             if not b_is_neither:
#                 audio_beep(freq=440, duration=500)
#                 print("Copied to clipboard -> ", data)
#                 pyperclip.copy(data)
#                 reference = data
#             else:
#                 audio_beep(freq=200, duration=750)
#                 pyperclip.copy(data_raw)
#
#         except Exception as e:
#             # print("[ERROR]: ", e, "\n")
#             audio_beep(freq=200, duration=750)
#             print("ERROR INVALID DATA", "\n")
