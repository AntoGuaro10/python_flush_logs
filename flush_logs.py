import subprocess
import os
import smtplib

# Function to locate the file containing the logs
# It checks the size of the file and it choose to delete or not the file and send an email
# It is based on the script flushlog.sh 
def flush(log_file):
    # You can costumize these variables
    size = 4096
    cmd = '/home/pi/./flushlog.sh'

    log_size = os.path.getsize(log_file)

    if(log_size >= size) :
        subprocess.call([cmd], shell = True)
        send_mail(0, log_size)
    else:
        cmd = 'echo "The log size is OK"'

        tmp = subprocess.call([cmd], shell=True)
        send_mail(1, log_size)

# Function called after flush() method to send an email alert
def send_mail(switch, size):
    # Choose the credentials that will be used for send the email
    # You should use a 2F-A enabled g-mail account ans setting up a 'Sign in with App Password'
    # It's recommended to see this doc from Google -> https://support.google.com/accounts/answer/185833?hl=en
    user = 'your.address@gmail.com'
    passwd = 'yourAppPassword'
    mail_object = 'Email generated from Pi flus_log script\n'

    if switch == 0:
        content = f'Hi Antonio, the log size was {size} so i flushed them'
    elif switch == 1:
        content = f'Hi Antonio, the log size ({size}) is OK'

    message = mail_object + content
    receiver = 'receiver.address@gmail.com'
    
    # Setting up the SMTP server to use and port
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()

    mail.login(user, passwd)
    mail.sendmail(user, receiver, message)

    mail.close()

log_file = '/home/pi/.morninglog.txt'   # The file containing the logs

flush(log_file) # Main function that is executed