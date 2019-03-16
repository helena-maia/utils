import os
import sys

videos = os.listdir(sys.argv[1])

for v in videos:
    if os.stat(sys.argv[1]+v).st_size == 0:
        os.remove(sys.argv[1]+v)
