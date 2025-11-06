import smtplib, ssl

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("boladugamer@gmail.com", "vsdnmilichxkyiit")
print("OK!")
server.quit()