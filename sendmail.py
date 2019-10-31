# !/usr/bin/python3
# coding: utf-8

import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr
from email.utils import formataddr
import json

json_path = "config.json"

def send_mail(Title, Subject, Content):
    try:
        file = open(json_path, "rb")
        fileJson = json.load(file)
        from_email = fileJson["from_email"]
        from_email_pwd = fileJson["from_email_pwd"]
        to_email = fileJson["to_email"]
        smtp_server = fileJson["smtp_server"]
        smtp_server_port = fileJson["smtp_server_port"]
        file.close()
    except Exception as e:
        print("Exception found", format(e))


    msg = MIMEText(format_substance(Subject, Content), "html", "utf-8")
    msg["From"] = format_addr("%s" % (from_email))
    msg["To"] = format_addr("%s" % (to_email))
    msg["Subject"] = Header(Title, "utf-8").encode()
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_server_port)
        #server.set_debuglevel(1)
        server.login(from_email, from_email_pwd)
        server.sendmail(from_email, [to_email], msg.as_string())
        print("Send Ok!")
    except Exception as e:
        print("Exception found", format(e))

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))
def format_substance(Subject, Content):
    return "<html><body><h3>" + Subject + "</h3><p>" + Content + "</p></body></html>"

if __name__ == "__main__":
    send_mail("Title", "Subject", "Content")
