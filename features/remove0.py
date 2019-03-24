import os

videos = os.listdir("rgb_of01_")

for v in videos:
    path = os.path.join("rgb_of01_", v)
    
    total = len(os.listdir(path))

    if(total == 0):
        os.rmdir(path)
