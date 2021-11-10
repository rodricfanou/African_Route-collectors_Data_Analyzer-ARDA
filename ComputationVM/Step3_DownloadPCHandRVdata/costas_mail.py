import smtplib
from email.mime.text import MIMEText
import sys
import re


def send_mail():

    usage = '''usage: <%s> <Destination email> <name> <subject> <message> <ticket>''' % (sys.argv[0])

    # Check input argument number
    if len(sys.argv) != 4:
        print(usage)
        exit(0)

    # Collect the arguments
    emailTo = sys.argv[1]
    subject = sys.argv[2]
    text = sys.argv[3]

    if not validateEmail(emailTo):
        print(0)
        exit(-1)
    
    gmailUser = '****@gmail.com'
    gmailPassword = '****'

    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = gmailUser
    msg['To'] = emailTo

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    #mailServer.ehlo()
    mailServer.starttls()
    #mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, emailTo, msg.as_string())
    mailServer.quit()
    print(1)
    exit(0)


def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return 1
    return 0

if __name__ == "__main__":
    send_mail()
