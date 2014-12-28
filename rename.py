import os
import exifread
import string

badones = []

# originals = '/Volumes/Backup/Pictures'
#destination = "/Volumes/Backup/pix"

#originals = '/Users/montyzukowski/personal/pix'
#destination = '/Users/montyzukowski/Dropbox/FamilyShared/Photos/2014 Family Photos'

originals = '/Users/montyzukowski/Google Drive/Photo Archives/origs/Pictures/2001/01/01'
#originals = '/Users/montyzukowski/personal/pix'
destination = '/Users/montyzukowski/Google Drive/Photo Archives/'

if not os.path.exists(destination):
    os.mkdir(destination)

useMonthDayDir = False
useMonthDir = True

ltrs = string.ascii_letters + string.digits


def generate_suffix(time, i=0):
    hours, mins, secs = time.split(":")
    h = int(hours)
    m = int(mins)
    s = int(secs) + i
    if s >= len(ltrs):
        s -= len(ltrs)
        m += 1
    if m >= len(ltrs):
        m -= len(ltrs)
        h += len(ltrs)
    return ltrs[h] + ltrs[m] + ltrs[s]

dt_fn_map = {}


def movePicture(dt, fn, destination):
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
    #os.rename(fn, dest)
    print 'saved', dest


for root, dirs, files in os.walk(originals):
    print 'processing', root
    for name in files:
        if not (name.endswith(".jpg") or name.endswith(".jpeg")
                or name.endswith(".JPG") or name.endswith(".JPEG")):
            continue
        if 'Thumbs' in root:
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
                dt_fn_map[dt] = fn
            else:
                print 'no exif info for', fn
                badones.append(fn)
        except Exception, e:
            badones.append(fn)
            print e
        f.close()

keys = dt_fn_map.keys()
print 'sorting', len(keys), 'keys'
keys.sort()
for key in keys:
    movePicture(key, dt_fn_map[key], destination)

for fn in badones:
    print "couldn't deal with", fn
