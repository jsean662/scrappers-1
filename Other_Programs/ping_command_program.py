from subprocess import call
import smtplib

call(['ping', 'www.oyeok.in/'])
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login('vipulmalhotra511@gmail.com', 'rahul1234')
server.sendmail('vipulmalhotra511@gmail.com', 'nimbalkarvicky9@gmail.com', 'Test mail')
server.sendmail('vipulmalhotra511@gmail.com', 'nimbalkarvicky9@gmail.com', 'Test mail')
server.quit()
