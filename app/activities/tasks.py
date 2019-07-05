from . import utils
from django.core.mail import EmailMessage
from background_task import background
from datetime import datetime


@background(schedule=5)
def email_report(subject, message, sender, recipient,
                 s_day, s_month, s_year, e_day, e_month, e_year, model):

    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    email = EmailMessage(
        subject,
        message,
        sender,
        [recipient])

    csv = utils.generate_csv(start_date, end_date, model)
    pdf = utils.generate_pdf(start_date, end_date, model)

    name = f"{model}-{start_date} {end_date}"

    email.attach(f"{name}.csv",
                 csv.csv,
                 "text/csv")
    email.attach(f"{name}.pdf",
                 pdf.getvalue(),
                 "text/pdf")
    email.send()
