import smtplib
 
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
s.starttls()
 
# Authentication
s.login("ashrithjacob2@gmail.com", "icdattc@123")
 
# message to be sent
message = "Message_you_need_to_send"
 
# sending the mail
s.sendmail("ashrithjacob2@gmail.com", "ashrithjacob@gmail.com", message)
 
# terminating the session
s.quit()