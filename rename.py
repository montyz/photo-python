import os
import time
import datetime
import exifread
import string

badones = []

# originals = '/Volumes/Backup/Pictures'
#destination = "/Volumes/Backup/pix"

#originals = '/Users/montyzukowski/personal/pix'
#destination = '/Users/montyzukowski/Dropbox/FamilyShared/Photos/2014 Family Photos'

originals = '/Users/montyzukowski/Google Drive/Photo Archives/origs/'
destination = '/Users/montyzukowski/Google Drive/Photo Archives/'

if not os.path.exists(destination):
    os.mkdir(destination)

useMonthDayDir = False
useMonthDir = True

ltrs = string.ascii_letters + string.digits


def generate_suffix(time, i=0):
    try:
        hours, mins, secs = time.split(":")
        h = int(hours)
        m = int(mins)
        s = int(secs) + i
        while s >= len(ltrs):
            s -= len(ltrs)
            m += 1
        if m >= len(ltrs):
            m -= len(ltrs)
            h += 1
        return ltrs[h] + ltrs[m] + ltrs[s]
    except IndexError:
        print h, m, s
        return "bad-"+h+m+s

dt_fn_map = {}


def movePicture(dt, fn, destination):
    print dt, fn, destination
    date, time = dt.split()
    year, month, day = date.split(":")
    i = 0
    destdir = os.path.join(destination, year)
    if not os.path.exists(destdir):
        os.mkdir(destdir)
    if useMonthDayDir:
        destdir = os.path.join(destdir, '%s-%s' % (month, day))
        if not os.path.exists(destdir):
            os.mkdir(destdir)
    if useMonthDir:
        destdir = os.path.join(destdir, '%s' % (month))
        if not os.path.exists(destdir):
            os.mkdir(destdir)
    dest = os.path.join(destdir, '%s-%s-%s-%s.jpg' % (year, month, day, generate_suffix(time)))
    while os.path.exists(dest):
        i = i + 1
        dest = os.path.join(destdir, '%s-%s-%s-%s.jpg' % (year, month, day, generate_suffix(time, i)))
    print 'saving', fn, 'to', dest
    os.rename(fn, dest)

    print 'saved', dest


for root, dirs, files in os.walk(originals):
    i = 0
    for name in files:
        if not (name.endswith(".jpg") or name.endswith(".jpeg")
                or name.endswith(".JPG") or name.endswith(".JPEG")):
            continue
        if 'Thumbs' in root or 'Thumbnails' in root:
            print 'Skipping', root
            continue
        fn = os.path.join(root, name)

        # Open image file for reading (binary mode)
        f = open(fn, 'rb')

        # Return Exif tags
        try:
            tags = exifread.process_file(f)
            if tags.has_key("EXIF DateTimeOriginal"):
                dt = tags["EXIF DateTimeOriginal"].printable
                '''if not dt.strip():
                    dt = tags["Image DateTime"].printable
                '''
            else:
                obj = datetime.datetime.fromtimestamp(os.path.getmtime(fn))
                print fn, 'creation time', obj
                dt = obj.isoformat(' ')
                dt = dt.replace('-', ':')
            if ':' in dt:
                dt_fn_map[dt] = fn
                i += 1
        except Exception, e:
            badones.append(fn)
            print e
        f.close()
    if i:
        print 'processing', root, i

print dt_fn_map

keys = dt_fn_map.keys()
print 'sorting', len(keys), 'keys'
keys.sort()
for key in keys:
    movePicture(key, dt_fn_map[key], destination)

for fn in badones:
    print "couldn't deal with", fn
