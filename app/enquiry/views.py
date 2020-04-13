import random
import names
from . import forms, models
from activities.utils import random_ints
from django.shortcuts import render
from django.contrib.auth import decorators

from django.http import HttpResponse

from pyexcelerate import Workbook, Style, Font
# cache key format <model name in uppercase>-<start-date>-<end-date>


def payments_list(request):
    return render(request, "enquiry/payments.html")


@decorators.login_required
def ota_detail(request, pk):
    obj_data = models.OTA.objects.get(pk=pk)
    form = forms.OTAForm(instance=obj_data)
    return render(request, "enquiry/ota_detail.html", {"form": form,
                                                       "title": obj_data.name})


@decorators.login_required
def partner_detail(request, pk):
    obj_data = models.Partner.objects.get(pk=pk)
    form = forms.PartnerForm(instance=obj_data)
    return render(request, "enquiry/partner_detail.html",
                  {"form": form,
                   "title": obj_data.name})


@decorators.login_required
def review_detail(request, pk):
    obj_data = models.Review.objects.get(pk=pk)
    form = forms.ReviewForm(instance=obj_data)
    return render(request, "enquiry/review_detail.html",
                  {"form": form,
                   "title": obj_data.headline})


@decorators.login_required
def ota_list(request):
    return render(request, "enquiry/ota_list.html", {"form": forms.OTAForm()})


@decorators.login_required
def partner_list(request):
    return render(request, "enquiry/partner_list.html",
                  {"form": forms.PartnerForm()})


@decorators.login_required
def review_list(request):
    return render(request, "enquiry/review_list.html",
                  {"form": forms.ReviewForm()})


@decorators.login_required
def export_users_csv(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="master_data_sample_1.xlsx"'
    headers = ['Sr. No', 'Booking Date ', ' Guest Name ', 'Email Id', 'Contact No', 'Web Site ', 'Check-in ',
               'Check-Out',
               'NO. Of  Adults', 'Stay Period', 'No of Rooms', 'Room Nights', 'Room Nos', ' Total Tax ',
               'Commission Amt  ', 'Supplier Amt ', 'Advance Date', ' Advance  Amt  ', 'Room Bill ',
               'Food Bill ', 'Taxi', 'Drink', ' Discount ', 'Total', 'Cash', 'Status',
               'Per Day Room Charges Realised', 'BaNK']

    wb = Workbook()
    ws = wb.new_sheet("Master data Feb - 2020")
    ws[1].value = [['MVR']]
    ws[2].value = [['01-01-2020']]
    ws.range("A1", "Z1").merge()
    ws[1][1].style.font.bold = True
    ws[1][1].style.font.size = 22
    ws[1][1].style.alignment.horizontal = "center"
    ws.set_row_style(1, Style(size=30))
    ws.range("A2", "Z2").merge()
    ws[2][1].style.alignment.horizontal = "center"
    ws[2][1].style.font.bold = True
    ws.range("A3", "Z3").merge()
    ws[3].value = []
    ws[4].value = [headers]
    ws.set_row_style(4, Style(size=25, font=Font(bold=True)))
    ws.set_col_style(list(range(1, 29)), Style(size=-1))
    print(ws.num_rows, ws.num_columns)

    data_list = []
    for i in range(1, 4):
        data = [None] * ws.num_columns
        data[0] = i
        booking_date = random.randint(1, 31)
        checkin_date = random.randint(1, 31)
        data[1], data[6], data[7], data[16] = [f"{i}-04-20" for i in random_ints(4, 1, 31)]
        data[2] = names.get_full_name()
        data[5] = random.choice(['go-mmt', 'direct', 'booking.com'])
        data[7] = random.choice(['A-2', 'K-2', 'K-1'])
        data[9], data[10], data[11] = random_ints(3)
        data[12] = random.choice(["R1", "R2", "R3"])
        data[17], data[18], data[19], data[20], \
        data[23], data[24], data[26], data[27], \
            = [random.randint(1000, 5000)
               for _ in range(8)]
        data[25] = "Done"
        data_list.append(data)
    # print(data_list)
    ws[5:7].value = data_list

    ws[8].value = [['Total']]
    ws.range("A8", "I8").merge()
    ws[8][1].style.font.bold = True
    ws[8][1].style.font.size = 16
    ws[8][1].style.alignment.horizontal = "center"
    ws.set_cell_value(8, 10, "=SUM(J5,J7)")
    ws.set_cell_value(8, 11, "=SUM(K5,K7)")
    ws.set_cell_value(8, 17, "=SUM(L4,L6)")
    ws.set_cell_value(8, 18, "=SUM(S5,S7)")
    ws.set_cell_value(8, 19, "=SUM(T5,T7)")
    ws.set_cell_value(8, 20, "=SUM(U5,U7)")

    new_headers = ['Sr. No.', 'DESCRIPTION', 'NO OF ROOMS', ' ', ' ', 'DAYS IN MONTH', '100% CAPACITY ROOM NIGHTS',
                   'ROOMS NIGHTS USED',
                   'CAPACITY UTILISATION', 'RATE REALISATION']

    ws[11].value = [['ANALYSIS']]

    ws.range("A11", "J11").merge()
    ws[11][1].style.font.bold = True
    ws[11][1].style.font.size = 14
    ws[11][1].style.alignment.horizontal = "center"
    ws[12].value = [new_headers]
    ws[13].value = []
    ws[14].value = [[' ', ' ROOMS ANALYSIS']]
    ws[14][2].style.font.bold = True
    ws.set_row_style(12, Style(size=35, font=Font(bold=True)))
    ws.set_col_style(list(range(1, 27)), Style(size=-1))
    ws[17].value = [['', 'RESTAURANT ANALYSIS']]
    ws[17][2].style.font.bold = True
    ws.set_row_style(20, Style(size=20))

    new_list = []
    for i in range(1, 3):
        data = [None] * ws.num_columns
        data[0] = i
        data[1] = random.choice(['NO OF ROOMS', 'NO OF BUNGLOW'])
        data[2], data[5], data[6], data[7], data[7], data[9] = random_ints(6, stop=1000)
        new_list.append(data)
        # print(new_list)
        ws[15:16].value = new_list

    sec_list = []
    for i in range(1, 4):
        data = [None] * ws.num_columns
        data[0] = i
        data[1] = random.choice(['FOOD BILL', 'AVERAGE PER DAY', 'AVERAGE PER NIGHT'])
        data[2], data[5], data[6], data[7], data[7], data[9] = random_ints(6, stop=1000)
        sec_list.append(data)
        ws[18:20].value = sec_list

    # New worksheet
    ws1 = wb.new_sheet("Bank Reconcilitaion Feb -2020")

    first_headers = ['Customer Name', 'Stay Period', 'Check in', 'Check Out', 'Razorpay ( Direct Booking)',
                     'Razorpay Commission', 'Bank Credit ( B+3)', 'Bank Credit Date', 'ICICI Machine',
                     'ICICI Commission', 'Bank Credit', 'Bank Credit Date', 'Paytm', 'Paytm Commission',
                     'Bank Credit( CI-3 Days)', 'Bank Credit Date',
                     'Google Pay', 'Bank Credit', 'Bank Date', 'MMT', 'MMT Commission ', 'Bank Credit( CI-3 Days)',
                     'Bank Credit Date', 'Go Ibibo', 'Go Ibibo Commission',
                     'Bank Credit( CI-3 Days)', 'Bank Credit Date', 'Axis Rooms( Booking.com)', 'Axis Rooms Commission',
                     'Bank Credit(B+5)', 'Bank Credit Date', ' Direct Bank',
                     ' Atom', 'Atom Commission', 'Bank Credit ( S+1)', 'Bank Credit Date', 'M Swipe',
                     'M Swipe Commission',
                     'Bank Credit ( S+1)', 'Bank Credit Date', '', '']

    ws1.range("B2", "E2").value = [['CUSTOMER DETAILS']]
    ws1[2][2].style.font.bold = True
    ws1[2][2].style.alignment.horizontal = "center"
    ws1.range("B2", "E2").merge()

    ws1.range("F2", "AE2").value = [['PRE CHECK IN']]
    # ws1.set_cell_style(2, 3, Style(font=Font(bold=True)))
    ws1[2][6].style.font.bold = True
    ws1[2][6].style.alignment.horizontal = "center"
    ws1.range("F2", "AE2").merge()

    ws1.range("AH2", "AN2").value = [['POST CHECK IN']]
    ws1[2][34].style.font.bold = True
    ws1[2][34].style.alignment.horizontal = "center"
    ws1.range("AH2", "AN2").merge()
    ws1[2][42].value = 'Cash'
    ws1[3][1].value = ''
    ws1.range("B3", "AQ3").value = [first_headers]
    ws1[3][2].style.font.bold = True
    ws1.set_row_style(3, Style(size=30, font=Font(bold=True)))
    ws1.set_col_style(list(range(1, 43)), Style(size=-1))
    ws1.range("B7", "E7").value = [['Total']]
    ws1[7][2].style.font.bold = True
    ws1[7][2].style.alignment.horizontal = "center"
    ws1.range("B7", "E7").merge()
    ws1.set_cell_value(7, 10, "=SUM(J4,J6)")
    ws1.set_cell_value(7, 11, "=SUM(K4,K6)")
    ws1.set_cell_value(7, 12, "=SUM(L4,L6)")
    ws1.set_cell_value(7, 18, "=SUM(R4,R6)")
    ws1.set_cell_value(7, 19, "=SUM(S4,S6)")
    ws1.set_cell_value(7, 21, "=SUM(U4,U6)")
    ws1.set_cell_value(7, 22, "=SUM(V4,V6)")
    ws1.set_cell_value(7, 23, "=SUM(W4,W6)")
    ws1.set_cell_value(7, 25, "=SUM(Y4,Y6)")
    ws1.set_cell_value(7, 26, "=SUM(Z4,Z6)")
    ws1.set_cell_value(7, 27, "=SUM(AA4,AA6)")
    ws1.set_cell_value(7, 38, "=SUM(AL4,AL6)")
    ws1.set_cell_value(7, 39, "=SUM(AM4,AM6)")
    ws1.set_cell_value(7, 40, "=SUM(AN4,AN6)")
    ws1.set_cell_value(7, 42, "=SUM(AP4,AP6)")
    ws1.set_cell_value(7, 43, "=SUM(AQ4,AQ6)")
    ws1.set_row_style(7, Style(font=Font(bold=True)))
    one_list = []

    for i in range(1, 4):
        data = [None] * ws1.num_columns
        data[1] = names.get_full_name()
        data[2] = random.choice(['dom', 'Direct', 'GO-MMT', 'Booking.com'])
        data[3], data[4], data[7], data[12], data[16], data[19], data[23], data[27], data[31], data[40], data[41] = [
            f"{i}-04-20" for i in random_ints(11, 1, 31)
        ]
        data[9], data[10], data[11], \
        data[17], data[18], data[20], data[21], \
        data[22], data[24], data[25], data[26], \
        data[37], data[38], data[39], data[40], \
        data[42], \
            = [random.randint(1000, 5000)
               for _ in range(16)]
        one_list.append(data)
        ws1[4:6].value = one_list

    second_headers = ['  ', 'SALE AMT', 'COMMISSION AMT', 'AMT IN BANK']
    ws1.range("B11", "E11").value = [second_headers]
    ws1.set_col_style(list(range(1, 4)), Style(size=-1))
    ws1.set_row_style(11, Style(size=30, font=Font(bold=True)))

    two_list = []
    for i in range(1, 4):
        data = [None] * ws1.num_columns
        data[1] = names.get_full_name()
        data[2], data[3], data[4] = random_ints(3, stop=8000)
        two_list.append(data)
        ws1[12:14].value = two_list

    ws1[15][2].value = 'TOTAL'
    ws1[15][2].style.font.bold = True
    ws1.set_cell_value(15, 3, "=SUM(C12,C14)")
    ws1.set_cell_value(15, 4, "=SUM(D12,D14)")
    ws1.set_cell_value(15, 5, "=SUM(E12,E14)")
    wb.save(response)
    return response

