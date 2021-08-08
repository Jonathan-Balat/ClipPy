####### IMPORTING #######
from time import sleep
import pyperclip
import os
import winsound

Version = "2.1.1.0"

######## OTHER FUNCTIONS #########
def audio_beep(freq=320, duration=1000):
    winsound.Beep(freq, duration)


def get_raw_cities():
    data_raw = pyperclip.paste()
    data_raw = data_raw.split("\n")
    for idx in range(0, len(data_raw)):
        data_raw[idx] = data_raw[idx].replace("\r", "").lower()
    return data_raw


def get_cities():
    input("Please copy cities, then press enter")
    cities_list = []
    cities_raw = get_raw_cities()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Cities considered are: ")
    for city in cities_raw:
        print(city)
        cities_list.append(city.lower())
    return cities_list

def prompt_option():
    b_flag = True
    while b_flag:
        option = input("\nAre these the correct data?<Y/N>:").lower()

        if option == "y":
            b_flag = False
        elif option == "n":
            b_flag = True
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid option: only Y or N")
    return b_flag

def get_raw_data_2():
    data_raw = pyperclip.paste()

    data_raw = data_raw.replace("\n", " ")
    data_raw = data_raw.replace("\r", " ")
    data_raw = data_raw.replace("  ", " ")
    data_raw = data_raw.replace("  ", " ")

    return data_raw

# def get_raw_data():
#     data_raw = pyperclip.paste()
#
#     if ("\n" in data_raw) or ("\r" in data_raw):
#         # Remove Next line WS
#         data_raw = data_raw.split("\n")
#         # Remove Carriage Return WS
#         for idx in range(0, len(data_raw)):
#             data_raw[idx] = data_raw[idx].replace("\r", "")
#         data_raw = " ".join(data_raw)
#
#     data_raw = data_raw.replace("  ", " ")
#     data_raw = data_raw.replace("  ", " ")  #Filter double spacing twice
#     return data_raw


######## LINK FUNCTIONS ##########
def check_website(data):
    b_hit = False
    web_hits = ["www", "http", "https", ".com"]

    data = unpack(data)
    # b_hit goes high once first true is seen
    for hit in web_hits:
        b_hit = b_hit or (data.find(hit) != -1)

    return b_hit


def check_email(data):
    data = unpack(data)
    # b_hit goes high once first true is seen
    b_hit = (data.find("@") != -1)

    return b_hit


######## NUMBER FUNCTIONS #########
def check_number_address(data, tolerance=0.625):
    count_num = 0
    data_len  = len(data)
    for idx in data:
        count_num += idx.isnumeric()
    percent_num = float(count_num) / float(data_len)

    # Sample ratio of numbers over total len
    # (559) 441-7991   10/14  0.714
    # +1 559-441-7991  11/15  0.733
    # 559.441.7991     10/12  0.833
    # 559 - 441 - 7991 10/16  0.625
    if not((percent_num < tolerance) or (count_num < 10) or (data_len > 20)):
        result = "Number"
    elif (data_len >= 18) and (data_len < 130):
        result = "Address"
    else:
        result = "None"

    return result


######## ADDRESS FUNCTIONS #########
def unpack(data):
    if isinstance(data, list):
        if len(data) == 1:
            data = data[0]
    return data


def set_lower(data):
    if isinstance(data,list):
        for idx in range(0,len(data)):
            data[idx] = data[idx].lower()
    else:
        data = data.lower()
    return data


def set_upper(data):
    if isinstance(data,list):
        for idx in range(0,len(data)):
            data[idx] = data[idx].title()
    else:
        data = data.title()
    return data


def check_zip(data):
    count_num = 0
    for idx in data:
        count_num += idx.isnumeric()
    b_flag_valid = (count_num == 5)
    return b_flag_valid


# def remove_country(data):
#     US_list = ["us", "US", "usa", "USA", "united states", "united states of america"]
#     if data[-1] in US_list:
#         data = data[:-1]
#     return data


def remove_country_2(data):
    US_list = ["us", "usa", "united states", "united states of america"]
    for ref_item in US_list:
        idx_found = data.rfind(ref_item)
        if idx_found != -1:
            data = data.replace(ref_item, ' ')
            break
    return data

def get_state_zip_2(data):
    State_list = ["ca", "CA", "California", "CALIFORNIA", "california"]

    #Double Spacing guard
    data = data.replace("  ", " ")

    for ref_item in State_list:
        idx_found = data.rfind(ref_item)
        if idx_found != -1:
            # data = data.replace(ref_item, ' ')
            break


    if idx_found > -1:
        temp  = data[idx_found:]
        ZIP = ""
        for content in temp:
            ZIP += content if content.isnumeric() else ""
        STATE = "CA"
        data  = data[:idx_found]
    else:
        STATE = ""
        ZIP = ""

    if STATE == "" or ZIP == "":
        raise Exception

    return data, STATE, ZIP

# def get_state_zip(data):
#     State_list = ["ca", "CA", "California", "CALIFORNIA", "california"]
#     b_flag_found = False
#
#     #Double Spacing guard
#     temp = data[-1].replace("  ", " ")
#     # print("TEMP:", temp)
#     print(data)
#     idx_found = temp.rfind("ca")
#     if idx_found > -1:
#         STATE = "CA" if temp[idx_found:idx_found+2] in State_list else ""
#         ZIP = temp[idx_found+2:].replace(" ","") if check_zip(temp[idx_found+2:]) else ""
#         data = data[:-1]
#     elif idx_found == -1:
#         STATE = "CA"
#         ZIP = check_zip(temp[idx_found:])
#         data = data[:-1]
#     else:
#         STATE = ""
#         ZIP = ""
#
#     if STATE == "" or ZIP == "":
#         # print("HIT")
#         raise Exception
#
#     return data, STATE, ZIP


def get_city_address_2(data):
    idx_list = []

    for city in cities_list:
        idx_found = data.rfind(city)
        idx_list.append(idx_found) if idx_found > -1 else None
    idx = max(idx_list)  # Checks the right-most occurrence of finding the city.
    # print("AT:", idx, data[0:idx], "||", data[idx:])

    if idx > -1:  # Found
        ADDRESS = data[0:idx]
        CITY = data[idx:]
        data = []
    else:
        print("\nNot valid city")
        raise Exception

    return data, CITY, ADDRESS


# def get_city_address(data):
#     data = " ".join(data)
#     data = unpack(data)
#
#     idx_list = []
#     ADDRESS = []
#     CITY = []
#
#     for city in cities_list:
#         idx_found = data.rfind(city)
#         idx_list.append(idx_found) if idx_found > -1 else None
#
#     idx = max(idx_list)
#
#     print("AT:", idx, data[0:idx], "||", data[idx:])
#
#     if idx > -1:
#         ADDRESS = data[0:idx]
#         CITY = data[idx:]
#         data = []
#     else:
#         print("\nNot valid city")
#         raise Exception
#
#     return data, CITY, ADDRESS


####### MAIN FUNCTIONS #######

def parse_number(data):
    number = []

    for idx in data:
        number.append(idx) if idx.isnumeric() else None

    num = ''.join(number)
    num = num[1:] if len(num) > 10 else num
    data = "(" + num[-10:-7] + ") " + num[-7:-4] + '-' + num[-4:]

    return data


def parse_address_removal(data):
    data = data.replace(", ", " ")
    data = set_lower(data)
    data = data.replace("  ", " ")
    # print("\n\n\nSTART: ", data)

    # Remove US
    data = remove_country_2(data)
    # print("\nAFTER US:", data)

    # Splits State and ZIP
    data, STATE, ZIP = get_state_zip_2(data)
    # print("\nAFTER STATE&ZIP", data)
    # print(STATE)
    # print(ZIP)

    # Splits City and Address
    data, CITY, ADDRESS = get_city_address_2(data)
    # print("\nAFTER CITY&ADDR", data)
    # print(CITY)
    # print(ADDRESS)

    data = [set_upper(ADDRESS)] + [set_upper(CITY)] + [STATE] + [ZIP]
    data = '\t'.join(data).replace("  ", "")
    # print("END:", data)

    return data

# def parse_address(data):
#     data = data.split(", ")
#     data = set_lower(data)
#     # print("\n\n\nSTART: ", data)
#
#     # Splits US
#     data = remove_country(data)
#     # print("\nAFTER US:", data)
#
#     # Splits State and ZIP
#     data, STATE, ZIP = get_state_zip(data)
#     # print("\nAFTER STATE&ZIP", data)
#     # print(STATE)
#     # print(ZIP)
#
#     # Splits City and Address
#     data, CITY, ADDRESS = get_city_address(data)
#     # print("\nAFTER CITY&ADDR", data)
#     # print(CITY)
#     # print(ADDRESS)
#
#     data = [set_upper(ADDRESS)] + [set_upper(CITY)] + [STATE] + [ZIP]
#     data = '\t'.join(data).replace("  ","")
#     # print("END:", data)
#
#     return data


def parse_link(data):
    if len(unpack(data)) < 100:
        result = "Web" if check_website(data) else "None"
        result = "Email" if check_email(data) else result
    else:
        result = "None"
    return result



################################ MAIN LOOP ################################
# STEP1 : Get City list
b_unfinished = True
while b_unfinished:
    os.system('cls' if os.name == 'nt' else 'clear')
    cities_list = get_cities()
    b_unfinished = prompt_option()

os.system('cls' if os.name == 'nt' else 'clear')

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
            # Step 1: Parse data
            # Collects data into a list until no more line
            data_raw  = get_raw_data_2()
            reference = get_raw_data_2()
            data = data_raw.lower()

            # Step 2: Checks for empty data
            if 1 > len(data):
                raise Exception  # Ends this current iteration, and waits for new data

            # Step 3: Clears Display for new data
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Data entered -> ", data)

            # Step 4: Check if Email or website
            b_is_what = parse_link(data)

            # Step 5: Classify data as number or address
            b_is_what = check_number_address(data) if b_is_what == "None" else b_is_what
            if b_is_what == "Number":
                print(b_is_what)
                data = parse_number(data)
            elif b_is_what == "Address":
                print(b_is_what)
                data = parse_address_removal(data)
            elif b_is_what == "Email" or b_is_what == "Web":
                print(b_is_what)
            else:
                print("NEITHER")
                b_is_neither = True

            if not b_is_neither:
                audio_beep(freq=440, duration=500)
                print("Copied to clipboard -> ", data)
                pyperclip.copy(data)
                reference = data
            else:
                audio_beep(freq=200, duration=750)
                pyperclip.copy(data_raw)

        except Exception as e:
            # print("[ERROR]: ", e, "\n")
            audio_beep(freq=200, duration=750)
            print("ERROR INVALID DATA", "\n")

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
