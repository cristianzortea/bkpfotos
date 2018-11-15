import smtplib
import os, shutil
import imghdr
import time
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime  


pathdropbox = "/home/tonho/Dropbox/Camera Uploads"
pathlog = "/home/tonho/bkpfotos"
pathbkp = "/home/tonho/bkpfotos/bkp"

def get_meta_picture(picture):
    ret = {}
    i = Image.open(picture)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
        #print("\n\n\n\n -----: ")
        #print(decoded)
        #print(value)
    return ret


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
	unsavefiles = []
	os.chdir(pathdropbox)
	print("readPictures ")
	for root, dirs, files in os.walk("."):  
		for filename in files:
			picturepath = pathdropbox + root.replace(".", "") + "/" + filename
			print("picturepath " + picturepath)
			unsavefiles.append(picturepath)
			#insertLog(picturepath)
			
	return unsavefiles

def sendemailfilescopied(emailfiles):
	text = "\n\n\n The listed files were copied to bkp:\n \n "
	for file in emailfiles:
		text = text + file
		#print(file)
	#sendemail(text)
	print(text)

def getfiledate(file):
	type_file = imghdr.what(file)
	print(type_file)
	date = None
	if type_file != None:
		print("pass")
		meta = get_meta_picture(file)
		datestring = meta['DateTimeOriginal'] 
		date = datetime.strptime(datestring,'%Y:%m:%d %H:%M:%S')
	return date

def executebkp():
	emailfiles = []
	#log = readLog()
	#files = log.split("\n")
	# get files
	correntDate = datetime.now()
	insertLog(" ---------------------- BKP: " + str(correntDate))
	unsavefiles = readPictures()
	for file in unsavefiles:
		print("line " + file)
		if file != "":
			date = getfiledate(file)
			dest = pathbkp
			if date != None:
				dest = dest + "/" + str(date.year) + "/" + str(date.month)
			shutil.copyfile(file, dest)
			insertLog("|_________ File: " + file)
			insertLog("          |___ Destination: " + dest)
			emailfiles.append("\n|_________ File: " + file)
			emailfiles.append("\n           |___ Destination: " + dest)
	
	sendemailfilescopied(emailfiles)

#while 1:
#    executebkp()
#    time.sleep(1000000)

executebkp()






