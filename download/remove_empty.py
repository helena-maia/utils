import os
import sys

videos = os.listdir(sys.argv[1])

for v in videos:
    path = os.path.join(sys.argv[1],v)
    if os.stat(path).st_size == 0:
        os.remove(path)
