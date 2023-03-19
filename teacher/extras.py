
import smtplib,secrets,string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from erp.settings import password,sender

def create_password(user)->bool:

    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars
    pwd=''
    for _ in range(8):
        pwd += ''.join(secrets.choice(alphabet))
    setattr(user,'pwd',pwd)
    #for adding user to group
    user.save()
    #sending mails
    
    if not receiver:
        try:
            receiver=user.email
        except:
            receiver=user.personalEmail
        
    user=user.name
    user=user.title()
    email_body="Hello "+user+"\nYour password for erp portal is "+pwd+"\nThank you!"
    message=MIMEMultipart('alternative',None,[MIMEText(email_body,'text')])
    message['Subject']="Regarding ERP password"
    message['From']=sender
    message['To']=receiver
    try:
        server=smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(sender,password)
        server.sendmail(sender,receiver,message.as_string())
        server.quit()
    except:
        return False
