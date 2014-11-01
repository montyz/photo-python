import os
import exifread

badones = []

#originals = '/Volumes/Backup/Pictures'
#destination = "/Volumes/Backup/pix"

originals = '/Users/montyzukowski/personal/2014 Family Photos'
destination = "/Users/montyzukowski/personal/pix"

useMonthDayDir = False

def generate_suffix(i):
    a = ord("a")
    z = ord("z")
    base = z-a+1
    lo = i % base
    hi = i / base
    return chr(a + hi) + chr(a + lo)


for root, dirs, files in os.walk(originals):
    for name in files:
        if not (name.endswith(".jpg") or name.endswith(".jpeg")
                or name.endswith(".JPG") or name.endswith(".JPEG")):
            continue
        fn = os.path.join(root, name)
        # Open image file for reading (binary mode)
        f = open(fn, 'rb')

        # Return Exif tags
        try:
            tags = exifread.process_file(f)
            if tags.has_key("EXIF DateTimeOriginal"):
                dt = tags["EXIF DateTimeOriginal"].printable
                date, time = dt.split()
                year, month, day = date.split(":")
                i=0
                destdir = os.path.join(destination, year)
                if not os.path.exists(destdir):
                    os.mkdir(destdir)
                if useMonthDayDir:
                    destdir = os.path.join(destdir, '%s-%s' % (month, day))
                    if not os.path.exists(destdir):
                        os.mkdir(destdir)
                dest = os.path.join(destdir, '%s-%s-%s.jpg' % (month, day, generate_suffix(i)))
                while os.path.exists(dest):
                    i=i+1
                    dest = os.path.join(destdir, '%s-%s-%s.jpg' % (month, day, generate_suffix(i)))
                os.rename(fn, dest)
                print 'saved', dest
            else:
                print 'no exif info for', fn
                badones.append(fn)
        except Exception, e:
            badones.append(fn)
            print e
        f.close()

for fn in badones:
    print "couldn't deal with", fn
