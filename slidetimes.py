import glob

import os
import time
from stat import *

fns = glob.glob("/Volumes/PATRIOT/*.jpg")
fns.sort()

new_mtime = 1415374978

for f in fns:
    st = os.stat(f)
    atime = st[ST_ATIME]  # access time
    mtime = st[ST_MTIME]  # modification time

    print f, mtime

    # modify the file timestamp
    #os.utime(f, (atime, new_mtime))
    new_mtime += 10
