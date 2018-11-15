
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime  
 
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



metadata = get_exif("/home/tonho/Dropbox/Camera Uploads/2013/2013-03-13 17.11.10.jpg")


datetimestring = metadata['DateTimeOriginal']
                                 
datetimeobject = datetime.strptime(datetimestring,'%Y:%m:%d %H:%M:%S')       
print (datetimeobject)  
print (datetimeobject.month)
print (datetimeobject.year)            




