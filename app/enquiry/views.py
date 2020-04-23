from . import forms, models
from django.shortcuts import render
from django.contrib.auth import decorators

from django.http import HttpResponse

from pyexcelerate import Workbook, Style, Font
import requests

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


def master_download(request):
    return render(request, "enquiry/master_data.html")


def excel_apply_formula(sheet, t_row, col_ind: iter, n_columns: iter, operation, s_row, e_row):
    for i in range(len(col_ind)):
        sheet.set_cell_value(
            t_row, col_ind[i], f"={operation}({n_columns[i]}{s_row}:{n_columns[i]}{e_row})"
        )


@decorators.login_required
def export_master_excel(request, month, year):

    # paymentautoaudit is the name of the other container running separately on port 8000
    res = requests.get(f"http://paymentautoaudit:8000/masterdata/{month}/{year}")
    data = res.json()
    print(res.status_code)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{data["metadata"]["filename"]}"'

    wb = Workbook()
    ws = wb.new_sheet(data["metadata"]["tab1_name"])
    ws[1].value = [['MVR']]
    ws[2].value = [[f'01-{month}-{year}']]
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

    t1_row_end = 5 + len(data["tab1_table1"]["data"][0].keys()) - 1
    ws[5:t1_row_end].value = data["tab1_table1"]["data"][0].values()

    ws[t1_row_end+1].value = [['Total']]
    ws.set_row_style(t1_row_end+1, Style(size=25, font=Font(bold=True),))
    ws.range(f"A{t1_row_end+1}", f"I{t1_row_end+1}").merge()
    ws[t1_row_end+1][1].style.font.bold = True
    ws[t1_row_end+1][1].style.alignment.horizontal = "center"
    excel_apply_formula(ws, t1_row_end+1, (10, 11, 12, 18, 19, 20),
                        ("J", "K", "L", "S", "T", "U"), "SUM", 5, t1_row_end)

    t2_start = ws.num_rows + 2

    ws[t2_start+1].value = [['ANALYSIS']]

    ws.range(f"A{t2_start+1}", f"J{t2_start+1}").merge()
    ws[t2_start+1][1].style.font.bold = True
    ws[t2_start+1][1].style.font.size = 14
    ws[t2_start+1][1].style.alignment.horizontal = "center"
    ws[t2_start+2].value = [data["tab1_table2"]["headers"]]
    ws[t2_start+3].value = []
    ws[t2_start+4].value = [[' ', ' ROOMS ANALYSIS']]
    ws[t2_start+4][2].style.font.bold = True
    ws.set_row_style(t2_start+2, Style(size=35, font=Font(bold=True)))
    ws.set_col_style(list(range(1, 27)), Style(size=-1))
    ws[t2_start+7].value = [['', 'RESTAURANT ANALYSIS']]
    ws[t2_start+7][2].style.font.bold = True
    ws.set_row_style(t2_start+10, Style(size=20))

    ws[t2_start+5:t2_start+6].value = [data["tab1_table2"]["data"][0]["row1"], data["tab1_table2"]["data"][0]["row2"]]
    ws[t2_start+8:t2_start+10].value = [data["tab1_table2"]["data"][0]["row3"], data["tab1_table2"]["data"][0]["row4"],
                                        data["tab1_table2"]["data"][0]["row5"]]

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
    tt1_row_end = 4 + len(data["tab2_table1"]["data"][0].keys()) - 1
    ws1.range(f"B{tt1_row_end+1}", f"E{tt1_row_end+1}").value = [['Total']]
    ws1[tt1_row_end+1][2].style.font.bold = True
    ws1[tt1_row_end+1][2].style.alignment.horizontal = "center"
    ws1.range(f"B{tt1_row_end+1}", f"E{tt1_row_end+1}").merge()

    excel_apply_formula(ws1, tt1_row_end+1,
                        [10, 11, 12, 18, 19, 21, 22, 23, 25, 26, 27, 38, 39, 40, 42, 43],
                        ["J", "K", "L", "R", "S", "U", "V", "W", "Y", "Z", "AA", "AL", "AM", "AN", "AP", "AQ"],
                        "SUM", s_row=4, e_row=tt1_row_end)

    formula_string = "=N{0}+U{0}+Y{0}+AC{0}+AG{0}+AH{0}+AL{0}+AP{0}"
    for i in range(4, tt1_row_end):
        ws1.set_cell_value(i, 43, formula_string.format(i))
    ws1.set_row_style(tt1_row_end+1, Style(font=Font(bold=True)))

    ws1[4:tt1_row_end].value = data["tab2_table1"]["data"][0].values()

    tt2_start = ws1.num_rows + 3
    ws1.range(f"B{tt2_start+1}", f"E{tt2_start+1}").value = [data["tab2_table2"]["headers"]]
    ws1.set_col_style(list(range(1, 4)), Style(size=-1))
    ws1.set_row_style(tt2_start+1, Style(size=30, font=Font(bold=True)))

    ws1[tt2_start+2:tt2_start+11].value = data["tab2_table2"]["data"][0].values()
    print(data["tab2_table2"]["data"][0].values())

    ws1[ws1.num_rows+1][2].value = 'TOTAL'
    ws1[ws1.num_rows][2].style.font.bold = True

    excel_apply_formula(ws1, tt2_start+12, [3, 4, 5], ["C", "D", "E"], "SUM", tt2_start+2, ws1.num_rows-1)
    ws1.set_row_style(ws1.num_rows, Style(size=25, font=Font(bold=True)))
    wb.save(response)
    return response


if __name__ == "__main__":
    res = requests.get("http://localhost:8001/masterdata/")
    print(res.status_code)
