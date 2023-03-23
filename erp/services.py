import string
from secrets import choice
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .settings import password,sender
from .models import subjects, course

def get_first_subject()->subjects:
    try:
        return subjects.sub_obj.first()
    except:
        return None
    
def get_first_course()->course:
    try:
        return course.course_obj.first()
    except:
        return None
    
def generate_password()->str:
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars
    pwd=''
    for _ in range(8):
        pwd += ''.join(choice(alphabet))
    return pwd


def send_mail(receiver_email:str,email_body:str)->bool:

    print("in send mail")
    message=MIMEMultipart('alternative',None,[MIMEText(email_body,'text')])
    message['Subject']="Regarding ERP password"
    message['From']=sender
    message['To']=receiver_email
    try:
        server=SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(sender,password)
        server.sendmail(sender,receiver_email,message.as_string())
        server.quit()
        print("mail sent")
    except Exception as e:
        print("Mail could not be sent.")
        print(e)
        return False
    return True

def create_new_password(user)->str:
    try:
        pwd=generate_password()
    
        setattr(user,'pwd',pwd)
        user.save()
        try:
            id=user.teacherid
        except:
            id=user.studentid

        try:
            email=user.email
        except:
            email=user.personalEmail
        
        print(email,id)

        email_body="Hello "+str(user)+"\nYour details for MyGurukul portal at mygurukul.pythonanywhere.com are:\nID:"+id+"\nPassword:"+pwd+"\nThank you!"
        send_mail(email,email_body)
        print("new password created for",user)
        return pwd
    
    except Exception as e:
        print(e)
        return False