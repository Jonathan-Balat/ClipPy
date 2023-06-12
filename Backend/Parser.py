######## ADDRESS FUNCTIONS #########
def unpack(data):
    if isinstance(data, list):
        if len(data) == 1:
            data = data[0]
    return data


def set_lower(data):
    if isinstance(data,list):
        for idx in range(0, len(data)):
            data[idx] = data[idx].lower()
    else:
        data = data.lower()
    return data


def set_upper(data):
    if isinstance(data, list):
        for idx in range(0,len(data)):
            data[idx] = data[idx].title()
    else:
        data = data.title()
    return data


def check_zip(data):
    COUNT_USA_ZIP = 5
    count_num = 0
    for idx in data:
        count_num += idx.isnumeric()
    return count_num == COUNT_USA_ZIP


def remove_country(data):
    US_list = ["us", "usa", "united states", "united states of america"]
    for ref_item in US_list:
        idx_found = data.rfind(ref_item)
        if idx_found != -1:
            data = data.replace(ref_item, ' ')
            break
    return data


def get_state_zip(data):
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


def get_city_address(data, cities_list):
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


def check_website(data):
    web_hits = ["www", "http", "https", ".com"]

    data = unpack(data)

    # b_hit goes high once first true is seen
    b_hit = False
    for hit in web_hits:
        b_hit |= (data.find(hit) != -1)

    return b_hit


def check_email(data):
    data = unpack(data)
    # b_hit goes high once first true is seen
    b_hit = (data.find("@") != -1)

    return b_hit


def parse_link(data):
    if len(unpack(data)) >= 100:  # 100 is a chosen boundary value for determining if it is a link
        data_type = "None"
    elif check_website(data):
        data_type = "Web"
    elif check_email(data):
        data_type = "Email"
    else:
        data_type = "None"

    # Step 5: Classify data as number or address
    if data_type == "None":
        check_number_address(data)

    return data_type


######## NUMBER FUNCTIONS #########
def check_number_address(data, tolerance=0.625):
    NUMBER_COUNT_MIN = 10
    NUMBER_DATA_LEN_MIN = 20
    ADDR_DATA_LEN_MAX = 130
    ADDR_DATA_LEN_MIN = 20
    count_num = 0

    # Counts the number of numbers for probability assessment below
    data_len  = len(data)
    for idx in data:
        count_num += idx.isnumeric()
    percent_num = float(count_num) / float(data_len)

    # NOTE: Below was derived on trial and error
    # Sample ratio of numbers over total len
    #   (559) 441-7991   10/14  0.714
    #   +1 559-441-7991  11/15  0.733
    #   559.441.7991     10/12  0.833
    #   559 - 441 - 7991 10/16  0.625
    if not((percent_num < tolerance) or (count_num < NUMBER_COUNT_MIN) or (data_len > NUMBER_DATA_LEN_MIN)):
        result = "Number"
    elif (data_len >= ADDR_DATA_LEN_MIN) and (data_len < ADDR_DATA_LEN_MAX):
        result = "Address"
    else:
        result = "None"

    return result


def identify_data(data):
    # Step 2: Checks for empty data
    if 1 > len(data):
        # raise Exception  # Ends this current iteration, and waits for new data
        data_type = "None"
    else:
        data = data.lower()

        data_type = parse_link(data)

    return data_type


##########  EXTRACTION METHODS  ##########
def parse_number(data):
    number = []

    for idx in data:
        number.append(idx) if idx.isnumeric() else None

    num = ''.join(number)
    num = num[1:] if len(num) > 10 else num
    data = "(" + num[-10:-7] + ") " + num[-7:-4] + '-' + num[-4:]

    return data


def parse_address(data, cities_list):
    # Remove commas and duplicate whitespaces
    data = data.replace(", ", " ")
    data = set_lower(data)
    data = data.replace("  ", " ")

    # print("\n\n\nSTART: ", data)

    # Remove US
    data = remove_country(data)
    # print("\nAFTER US:", data)

    # Splits State and ZIP
    data, STATE, ZIP = get_state_zip(data)
    # print("\nAFTER STATE&ZIP", data)
    # print(STATE)
    # print(ZIP)

    # Splits City and Address
    data, CITY, ADDRESS = get_city_address(data, cities_list)
    # print("\nAFTER CITY&ADDR", data)
    # print(CITY)
    # print(ADDRESS)

    data = [set_upper(ADDRESS)] + [set_upper(CITY)] + [STATE] + [ZIP]
    data = '\t'.join(data).replace("  ", "")
    # print("END:", data)

    return data


def extract_data(data, data_type, cities_list):
    if data_type == "Number":
        print(data_type)
        data = parse_number(data)

    elif data_type == "Address":
        print(data_type)
        data = parse_address(data, cities_list)

    elif data_type == "Email" or data_type == "Web":
        print(data_type)

    else:
        print("NEITHER")
        data = None

    return data

