import smtplib
server=smtplib.SMTP("smtp.office365.com",587)
server.starttls()
server.login("abhinav.19b111050@abes.ac.in","Abhi.abes")
server.sendmail("abhinav.19b111050@abes.ac.in","anand.19b111041@abes.ac.in","hii")
print("sent")
