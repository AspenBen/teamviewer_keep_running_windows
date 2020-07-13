from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_mail():
    account = "sourcexxxxx@163.com"#I resign a 163 emial as Outbox
    password = "GLKTJULVSQVMHBVE"
    to = "destinaitonxxxxx@asterfusion.com"#the mail we want to send
    smtp_server = "smtp.163.com"

    msg = MIMEMultipart()
    msg['From'] = _format_addr("sourcexxxx@163.com")
    msg['To'] = _format_addr("destinationxxxx@asterfusion.com")
    msg['Subject'] = Header('teamviwer ID and password')
    #content word
    msg.attach(MIMEText('teamviewer exit suddendly, now has restart it, please get the ID and password from under picture', 'plain', 'utf-8'))
 
    #picture
    with open('C:\\Users\\26989\\software\\teamviwer_auto_running\\account_pswd.jpg', 'rb') as f:
        mime = MIMEBase('image', 'jpeg', filename='account_pswd.jpg')
        mime.add_header('Content-Disposition', 'attachment', filename='account_pswd.jpg')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(account, password)
    server.sendmail(account, [to], msg.as_string())

    print ("the email has sended, check email box")

    server.quit()
