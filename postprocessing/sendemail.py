# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from helpers.helpers import get_mail_list, get_plots_path

def buy(stock_name, date):
    fromaddr = "waoustockinvest@gmail.com"
    emails = get_mail_list()
    toaddr = ', '.join( emails )

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Time to buy {}".format(stock_name)

    # string to store the body of the mail
    body = "Waou Invest would like to inform you that {0} had a golden cross today (the {1} ) ! \n Please see attachment!".format(stock_name, date)

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "{0}/goldencross{1}.png".format(get_plots_path(), stock_name.replace("/",""))
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "fre--erf")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, emails, text)

    # terminating the session
    s.quit()

def sell(stock_name, date):
    fromaddr = "waoustockinvest@gmail.com"
    emails = get_mail_list()
    toaddr = ', '.join( emails )

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Time to sell {}".format(stock_name)

    # string to store the body of the mail
    body = "Waou Invest would like to inform you that {0} had a dead cross today (the {1} ) ! \n Please see attachment!".format(stock_name, date)

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "{0}/deadcross{1}.png".format(get_plots_path(), stock_name.replace("/",""))
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "fre--erf")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, emails, text)

    # terminating the session
    s.quit()
