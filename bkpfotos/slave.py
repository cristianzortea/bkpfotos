import smtplib
import os, shutil
import imghdr
import time
import imaplib
import email

from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime 
from pathlib import Path 

class Gmail:

	USER = 'monitoralertmessage@gmail.com'  
	PWD = 'B4PPbTbQsr9NyCW'
	TO = ['cristianzortea@gmail.com', 'monitoralertmessage@gmail.com']
	SMTP_SERVER = "imap.gmail.com"
	SMTP_PORT = 993
	
	def sendemail(self, subject):
		try:  
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(self.USER, self.PWD)
			server.sendmail(self.gmail_user, self.TO, subject)
			server.close()
		except Exception as e:
			printlog("Error: %s!\n\n" % e)

	def read_email_from_gmail(self):
		#try:
			mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
			mail.login(self.USER, self.PWD)
			mail.select('inbox')

			type, data = mail.search(None, 'ALL')
			mail_ids = data[0]

			id_list = mail_ids.split()   
			first_email_id = int(id_list[0])
			latest_email_id = int(id_list[-1])

			for i in range(latest_email_id, first_email_id, -1):
				typ, data = mail.fetch(str(i), "(RFC822)" )
				for response_part in data:
					if isinstance(response_part, tuple):

					
						
						print("\n\n\n\n\n\n---------------------------------")
						myemail = email.message_from_string(response_part[1].decode()) 
						if myemail.is_multipart():
							for payload in myemail.get_payload():
								myemail = payload.get_payload()

						else:
							myemail = myemail.get_payload()

						print(myemail)

						#if self.USER == myemail['from']:
						#printlog("To : " + str(myemail['to']) + "\n")
						#printlog("Subject : " + str(myemail['subject']) + "\n")
						#printlog("From : " + str(myemail['from']) + "\n")
						#printlog("Body : " + str(myemail['body']) + "\n")
							
		#except Exception as e:
			#printlog("Error: %s!\n\n" % e)

pathdropbox = "/home/tonho/Dropbox/Camera Uploads"
pathlog = "/home/tonho/bkpfotos"
pathbkp = "/home/tonho/bkpfotos/bkp"

def createLog(text):
	os.chdir(pathlog)
	file = open("log.txt","w") 
	file.write(text) 
	file.close()

def get_meta_picture(picture):
    ret = {}
    i = Image.open(picture)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def printlog(text):
	print(text)
	os.chdir(pathlog)
	file = open("log.txt","a") 
	file.write(text + "\n") 
	file.close()

def readLog():
	os.chdir(pathlog)
	printlog('reading log!')
	file = open("log.txt", "r") 
	text = file.read() 
	file.close() 
	return text

def readPictures():
	printlog("Reading pictures... ")
	return os.listdir(pathdropbox)

def sendemailfilescopied(emailfiles):
	email = Email()
	text = "\n"
	if len(emailfiles) != 0:
		text = "\n\n\n The listed files were copied to bkp:\n"
		for file in emailfiles:
			text = text + file
	else:
		text = "\n\n\n There are no files to BKP.\n"

	email.sendemail(text)
	printlog(text)

def getfiledate(file):
	type_file = imghdr.what(file)
	date = None
	if type_file != None:
		meta = get_meta_picture(file)
		datestring = meta['DateTimeOriginal'] 
		date = datetime.strptime(datestring,'%Y:%m:%d %H:%M:%S')
	return date

def createdirectory(dir):
	destination = Path(dir)
	# Validate if the directory exists
	if not destination.is_dir():
		try:
			os.makedirs(dir)
		except OSError:
			printlog("Creaion of the directory %s failed" % dir)
		else:
			printlog("Successfully created the directory %s" % dir)


def savefiles(emailfiles, file, dest):
	os.chdir(pathdropbox)
	printlog("save files")
	# save file
	try:  
		shutil.move(file,dest)
		os.remove(file)
		printlog("|_________ File: " + file)
		printlog("          |___ Destination: " + dest)
		emailfiles.append("\n|_________ File: " + file)
		emailfiles.append("\n           |___ Destination: " + dest)
	except Exception as e:
		printlog("Error copying : %s!\n\n" % e)
		sendemail("Error copying : %s!\n\n" % e)

# BKP
def executebkp():
	emailfiles = []
	# get files
	correntDate = datetime.now()
	printlog("---------------------- BKP: " + str(correntDate))
	files = readPictures()
	for file in files:
		realfile = pathdropbox + "/" + file
		printlog("Get file " + realfile)
		date = getfiledate(realfile)
		dest = pathbkp
		if date != None:

			dest = dest + "/" + str(date.year) + "/" + str(date.month)
			createdirectory(dest)

		savefiles(emailfiles, realfile, dest)

	# send email
	sendemailfilescopied(emailfiles)

while 1:
	printlog("...")

	#executebkp()
	gmail = Gmail()
	gmail.read_email_from_gmail()
	# 10 seconds
	time.sleep(10)

#bkp executebkp()







