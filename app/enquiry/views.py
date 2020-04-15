from . import forms, models
from .master_data import provide_master_data
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
def export_master_excel(request):
    data = provide_master_data()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{data["metadata"]["filename"]}"'

    wb = Workbook()
    ws = wb.new_sheet(data["metadata"]["tab1_name"])
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
    ws[4].value = [data["tab1_table1"]["headers"]]
    ws.set_row_style(4, Style(size=25, font=Font(bold=True)))
    ws.set_col_style(list(range(1, 29)), Style(size=-1))

    ws[5:7].value = data["tab1_table1"]["data"][0].values()

    ws[8].value = [['Total']]
    ws.range("A8", "I8").merge()
    ws[8][1].style.font.bold = True
    ws[8][1].style.font.size = 16
    ws[8][1].style.alignment.horizontal = "center"
    ws.set_cell_value(8, 10, "=SUM(J5:J7)")
    ws.set_cell_value(8, 11, "=SUM(K5:K7)")
    ws.set_cell_value(8, 17, "=SUM(L4:L6)")
    ws.set_cell_value(8, 18, "=SUM(S5:S7)")
    ws.set_cell_value(8, 19, "=SUM(T5:T7)")
    ws.set_cell_value(8, 20, "=SUM(U5:U7)")

    ws[11].value = [['ANALYSIS']]

    ws.range("A11", "J11").merge()
    ws[11][1].style.font.bold = True
    ws[11][1].style.font.size = 14
    ws[11][1].style.alignment.horizontal = "center"
    ws[12].value = [data["tab1_table2"]["headers"]]
    ws[13].value = []
    ws[14].value = [[' ', ' ROOMS ANALYSIS']]
    ws[14][2].style.font.bold = True
    ws.set_row_style(12, Style(size=35, font=Font(bold=True)))
    ws.set_col_style(list(range(1, 27)), Style(size=-1))
    ws[17].value = [['', 'RESTAURANT ANALYSIS']]
    ws[17][2].style.font.bold = True
    ws.set_row_style(20, Style(size=20))

    ws[15:16].value = [data["tab1_table2"]["data"][0]["row1"], data["tab1_table2"]["data"][0]["row2"]]
    ws[18].value = [data["tab1_table2"]["data"][0]["row3"]]
    # ws[18:20].value = data["tab1_table2"]["data"][0].values()

    # New worksheet
    ws1 = wb.new_sheet(data["metadata"]["tab2_name"])

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
    ws1.range("B3", "AQ3").value = [data["tab2_table1"]["headers"]]
    ws1[3][2].style.font.bold = True
    ws1.set_row_style(3, Style(size=30, font=Font(bold=True)))
    ws1.set_col_style(list(range(1, 43)), Style(size=-1))
    ws1.range("B7", "E7").value = [['Total']]
    ws1[7][2].style.font.bold = True
    ws1[7][2].style.alignment.horizontal = "center"
    ws1.range("B7", "E7").merge()
    ws1.set_cell_value(7, 10, "=SUM(J4:J6)")
    ws1.set_cell_value(7, 11, "=SUM(K4:K6)")
    ws1.set_cell_value(7, 12, "=SUM(L4:L6)")
    ws1.set_cell_value(7, 18, "=SUM(R4:R6)")
    ws1.set_cell_value(7, 19, "=SUM(S4:S6)")
    ws1.set_cell_value(7, 21, "=SUM(U4:U6)")
    ws1.set_cell_value(7, 22, "=SUM(V4:V6)")
    ws1.set_cell_value(7, 23, "=SUM(W4:W6)")
    ws1.set_cell_value(7, 25, "=SUM(Y4:Y6)")
    ws1.set_cell_value(7, 26, "=SUM(Z4:Z6)")
    ws1.set_cell_value(7, 27, "=SUM(AA4:AA6)")
    ws1.set_cell_value(7, 38, "=SUM(AL4:AL6)")
    ws1.set_cell_value(7, 39, "=SUM(AM4:AM6)")
    ws1.set_cell_value(7, 40, "=SUM(AN4:AN6)")
    ws1.set_cell_value(7, 42, "=SUM(AP4:AP6)")
    ws1.set_cell_value(7, 43, "=SUM(AQ4:AQ6)")

    formula_string = "=N{0}+U{0}+Y{0}+AC{0}+AG{0}+AH{0}+AL{0}+AP{0}"
    for i in range(4, 7):
        ws1.set_cell_value(i, 43, formula_string.format(i))
    ws1.set_row_style(7, Style(font=Font(bold=True)))

    print(ws1.num_columns)
    print(len(tuple(data["tab2_table1"]["data"][0].values())[0]))
    ws1[4:6].value = data["tab2_table1"]["data"][0].values()

    ws1.range("B11", "E11").value = [data["tab2_table2"]["headers"]]
    ws1.set_col_style(list(range(1, 4)), Style(size=-1))
    ws1.set_row_style(11, Style(size=30, font=Font(bold=True)))

    ws1[12:14].value = data["tab2_table2"]["data"][0].values()

    ws1[15][2].value = 'TOTAL'
    ws1[15][2].style.font.bold = True
    ws1.set_cell_value(15, 3, "=SUM(C12:C14)")
    ws1.set_cell_value(15, 4, "=SUM(D12:D14)")
    ws1.set_cell_value(15, 5, "=SUM(E12:E14)")
    wb.save(response)
    return response
