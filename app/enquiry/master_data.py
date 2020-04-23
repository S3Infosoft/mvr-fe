import random
from activities.utils import random_ints
from names import get_full_name


def provide_master_data():
    """
    Provide sample data to populate all the values in the master data excel.
    Later on this structure would be provided by autoaudit API call.
    :return: dictionary of data to populate master data for excel report geenration.
    """
    data = {
        "metadata": {
            "filename": "master_data_sample_1.xlsx",
            "tab1_name": "Master data Feb - 2020",
            "tab2_name": "Bank Reconcilitaion Feb -2020"
        },
        "tab1_table1": {
            "headers": ['Sr. No', 'Booking Date ', ' Guest Name ', 'Email Id', 'Contact No', 'Web Site ', 'Check-in ',
                        'Check-Out', 'NO. Of  Adults', 'Stay Period', 'No of Rooms', 'Room Nights', 'Room Nos',
                        ' Total Tax ',
                        'Commission Amt  ', 'Supplier Amt ', 'Advance Date', ' Advance  Amt  ', 'Room Bill ',
                        'Food Bill ', 'Taxi', 'Drink', ' Discount ', 'Total', 'Cash', 'Status',
                        'Per Day Room Charges Realised', 'BanK'],
            "data": [{}]
        },
        "tab1_table2": {
            "headers": ['Sr.No.', 'Description', 'No of Rooms', '', '', 'Days in Month', '100% Capacity Room Nights',
                        'Rooms Nights Used', 'Capacity Utilisation', 'Rate Realisation'],
            "data": [{
                "row1": ['1', 'NO OF ROOMS', '12', '', '', '13', '550', '13', '60%', '34578.21'],
                "row2": ['2', 'NO OF BUNGLOW', '20', '', '', '3', '445', '10', '40%', '4008.91'],
                "row3": ['3', 'FOOD PER BILL', '', '', '', '3', '', '10', '', '40000'],
                "row4": ['4', 'AVERAGE PER DAY', '', '', '', '4', '', '12', '', '8000'],
                "row5": ['5', 'AVERAGE PER ROOM NIGHT', '', '', '', '8', '', '11', '','7000'],
            }]

        },
        "tab2_table1": {
            "headers": ['Customer Name', 'Stay Period', 'Check in', 'Check Out', 'Razorpay(Direct Booking',
                        'Razorpay Commission',
                        'Bank Credit(B+3)', 'Bank Crdit Date', 'ICICI Machine', 'ICICI Commission', 'Bank Credit',
                        'Bank Credit Date', 'Paytm', 'Paytm Commission', 'Bank Credit(CI-3 Days)', 'Bank Credit Date',
                        'Google Pay', 'Bank Credit', 'Bank Date', 'MMT', 'MMT Commission', 'Bank Credit(CI-3 Days)',
                        'Bank Credit Date', 'Go Ibibo', 'Go Ibibo Commission', 'Bank Credit(CI-3 Days)',
                        'Bank Credit Date', 'Axis Rooms(Booking.com)', 'Axis Rooms Commission', 'Bank Credit(B+5)',
                        'Bank Credit Date', 'Direct Bank', 'Atom', 'Atom Commission', 'Bank Credit(S+1)',
                        'Bank Credit Date', 'M Swipe', 'M Swipe Commission', 'Bank Credit(S+1)', 'Bank Credit Date',
                        '42', '43'],
            "data": [{}]

        },
        "tab2_table2": {
            "headers": ["", "SALE AMT",	"COMMISSION AMT", "AMT IN BANK"],
            "data": [{
                "row1": ['', 'RAZORPAY', '45637', '5347.78', '89756.4'],
                "row2": ['', 'MMT', '1700.2', '2345.89', '8000.65'],
                "row3": ['', 'Google Pay', '1800.2', '2345.89', '8000.65'],
                "row4": ['', 'ICICI Machine', '8000', '7634.67', '87345'],
                "row5": ['', 'MMT', '9000', '7634.67', '87345'],
                "row6": ['', 'GOIBIBO', '5900', '7634.67', '87345'],
                "row7": ['', 'AXIS ROOMS', '7000', '7634.67', '87345'],
                "row8": ['', 'DIRECT BANK', '4000', '74.67', '87345'],
                "row9": ['', 'ATOM', '5200', '9000', '87345'],
                "row10": ['', 'M SWIPE', '23000', '45678.67', '87345'],
            }]
        }
    }

    date_format = "{:02}-04-20"
    for i in range(1, 4):
        key = f"row{i}"
        values = [None] * len(data["tab1_table1"]["headers"])
        for j in range(len(data["tab1_table1"]["headers"])):
            if j == 0:
                values[j] = i
            elif j in (1, 6, 7, 16):        # for Dates
                values[j] = date_format.format(random_ints(1, stop=31)[0])
            elif j == 2:            # For Named
                values[j] = get_full_name()
            elif j in (3, 4, 13, 14, 15, 21, 22):       # For Blank entries
                values[j] = ""
            elif j == 5:      # For website
                values[j] = random.choice(["Direct", "Go-MMT", "Booking.com"])
            elif j == 8:
                values[j] = random.choice(["A1", "A3", "A5"])
            elif j in (9, 10, 11):
                values[j] = random_ints(1, stop=5)[0]
            elif j == 12:
                values[j] = random.choice(["R1", "B1"])
            elif j in (17, 18, 19, 20, 23, 24, 26, 27):
                values[j] = random_ints(1, start=1000, stop=5000)[0]
            elif j == 25:
                values[j] = "Done"
        data["tab1_table1"]["data"][0][key] = values

    # enteries for tab2 table1
    for i in range(1, 4):
        key = f"row{i}"
        values = [None] * len(data["tab2_table1"]["headers"])
        print(len(data["tab2_table1"]["headers"]))
        for j in range(len(data["tab2_table1"]["headers"])):
            if j == 1:
                values[j] = get_full_name()
            elif j in (0, 5, 6, 7, 13, 14, 15, 28, 29, 30, 32, 33, 34, 35):
                values[j] = ""
            elif j == 2:
                values[j] = random.choice(["Direct", "Booking.com", "Go-MMT"])
            elif j in(3, 4, 8, 12, 16, 19, 23, 27, 31, 36, 40):
                values[j] = date_format.format(random_ints(1, stop=31)[0])
            elif j in (9, 10, 11, 17, 18, 20, 21, 22, 24, 25, 26, 37, 38, 39, 41, 42):
                values[j] = random_ints(1, start=1000, stop=7000)[0]
        data["tab2_table1"]["data"][0][key] = values
        for header in data["tab2_table1"]["headers"]:
            print(header, end=" ")

    return data

    # TODO: Populate the data to create structure as expected for report generation.
    # return data


if __name__ == "__main__":
    provide_master_data()
