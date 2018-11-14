import smtplib
import os, shutil

pathdropbox = "/home/tonho/Dropbox/Camera Uploads"
pathlog = "/home/tonho/bkpfotos"
pathbkp = "/home/tonho/bkpfotos/bkp"

def sendemail(subject):
	print("Sending email")

	gmail_user = 'monitoralertmessage@gmail.com'  
	gmail_password = 'B4PPbTbQsr9NyCW'
	to = ['cristianzortea@gmail.com', 'monitoralertmessage@gmail.com']   

	try:  
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(gmail_user, to, subject)
		server.close()
		print ('Email sent!')
	except Exception as e:
		print("Error: %s!\n\n" % e)

def createLog(text):
	os.chdir(pathlog)
	print ('Creating log!')
	file = open("log.txt","w") 
	file.write(text) 
	file.close()
	print ('Created log!')

def insertLog(text):
	os.chdir(pathlog)
	print ('inserting log line: ' + text)
	file = open("log.txt","a") 
	file.write(text + "\n") 
	file.close()

def readLog():
	os.chdir(pathlog)
	print ('reading log!')
	file = open("log.txt", "r") 
	text = file.read() 
	file.close() 
	print ('read log!')
	return text

def readPictures():
	os.chdir(pathdropbox)
	for root, dirs, files in os.walk("."):  
		for filename in files:

				
			insertLog(filename)

def sendemailfilescopied():
	filescopied  = readLog()
	text = "\n\n\n The listed files were copied to bkp:\n \n " + filescopied
	sendemail(text)
	createLog("")

#createLog("teste")
readPictures()
sendemailfilescopied()





