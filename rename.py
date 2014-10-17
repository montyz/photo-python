import os
import exifread
import glob

files = glob.glob("/Users/montyzukowski/personal/2014 Family Photos/*.jpg")

for fn in files:
    # Open image file for reading (binary mode)
    f = open(fn, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    if tags.has_key("EXIF DateTimeOriginal"):
        dt = tags["EXIF DateTimeOriginal"].printable
        date, time = dt.split()
        year, month, day = date.split(":")
        i=1
        dest = os.path.join(os.path.dirname(fn), '%s-%s-%02d.jpg' % (month, day, i))
        while os.path.exists(dest):
            i=i+1
            dest = os.path.join(os.path.dirname(fn), '%s-%s-%02d.jpg' % (month, day, i))
        os.rename(fn, dest)
