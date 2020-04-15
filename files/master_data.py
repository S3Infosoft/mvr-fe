

def provide_master_data():
    """
    Provide sample data to populate all the values in the master data excel.
    Later on this structure would be provided by autoaudit API call.
    :return: dictionary of data to populate master data for excel report geenration.
    """
    print("Entered here")
    data = {
            "metadata": {
                "filename": "master_data_sample_1.xlsx",
                "tab1_name": "Master data Feb - 2020",
                "tab2_name": "Bank Reconcilitaion Feb -2020"
            },
            "tab1_table1": {
                "headers": ['Sr. No', 'Booking Date ', ' Guest Name ', 'Email Id', 'Contact No', 'Web Site ', 'Check-in ',
               'Check-Out','NO. Of  Adults', 'Stay Period', 'No of Rooms', 'Room Nights', 'Room Nos', ' Total Tax ',
               'Commission Amt  ', 'Supplier Amt ', 'Advance Date', ' Advance  Amt  ', 'Room Bill ',
               'Food Bill ', 'Taxi', 'Drink', ' Discount ', 'Total', 'Cash', 'Status', 'Per Day Room Charges Realised', 'BanK'],
                "data": [{
                    'row1': ['14-04-20', 'Kristel Conde', '', '', 'direct', '18-04-20', 'A-2', '', '31', '70', '63',
                             'R2', '', '', '', '25-04-20', '2354', '1451', '2114', '3164', '', '', '1261', '4926', 'Done', '3847', '2905'],
                    'row2': ['14-04-20', 'Kristel Conde', '', '', 'direct', '18-04-20', 'A-2', '', '31', '70', '63',
                             'R2', '', '', '', '25-04-20', '2354', '1451', '2114', '3164', '', '', '1261', '4926',
                             'Done', '3847', '2905'],
                    'row3': ['14-04-20', 'Kristel Conde', '', '', 'direct', '18-04-20', 'A-2', '', '31', '70', '63',
                             'R2', '', '', '', '25-04-20', '2354', '1451', '2114', '3164', '', '', '1261', '4926',
                             'Done', '3847', '2905'],
                }
                ]
            },
            "tab1_table2": {},
            "tab2_table1": {},
            "tab2_table2": {}
            }
    print(data["tab1_table1"])
    return data
