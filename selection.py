import random
import argparse
import os
import numpy as np

def getArgs():
    parser = argparse.ArgumentParser(description='Randomly select two rgb frames (one per half) and a stack of 10 optical flow images.')
    parser.add_argument("rgb_of_dir", action='store', type=str, help="directory with rgb frames and optical images")
    parser.add_argument("dest_dir", action='store', type=str, help="directory to copy selected images")
    return parser.parse_args()

args = getArgs()
random.seed(42)

rgb_fmt = "img_%05d.jpg"
of_fmt = "flow_%c_%05d.jpg"
index_list = ["video,rgb1,rgb2,of_start"]

if not os.path.isdir(args.dest_dir):
        print("creating folder: "+args.dest_dir)
        os.makedirs(args.dest_dir)

index_path = os.path.join(args.dest_dir,"index_list.txt")
missing_path = os.path.join(args.dest_dir, "missing.txt")
incomplete_path = os.path.join(args.dest_dir, "incomplete.txt")

for d in os.listdir(args.rgb_of_dir):
    path_orig = os.path.join(args.rgb_of_dir, d+"/")
    path_dest = os.path.join(args.dest_dir, d+"/")

    total = int(len(os.listdir(path_orig))/3)

    if(total >= 10):
        if not os.path.isdir(path_dest):
            print("creating folder: "+path_dest)
            os.makedirs(path_dest)

        rgb1 = random.randint(1,int(total/2))
        rgb2 = random.randint(int(total/2)+1,total)
        of = random.randint(1,total-10)
        index_list.append(d+","+str(rgb1)+","+str(rgb2)+","+str(of))

        rgb_orig = os.path.join(path_orig, rgb_fmt%(rgb1))
        rgb_dest = os.path.join(path_dest, rgb_fmt%(1))
        os.system("cp '"+rgb_orig+"' '"+rgb_dest+"'") 

        rgb_orig = os.path.join(path_orig, rgb_fmt%(rgb2))
        rgb_dest = os.path.join(path_dest, rgb_fmt%(2))
        os.system("cp '"+rgb_orig+"' '"+rgb_dest+"'")

        for i in range(10):
            of_orig = os.path.join(path_orig, of_fmt%('x',of+i))
            of_dest = os.path.join(path_dest, of_fmt%('x',i+1))
            os.system("cp '"+of_orig+"' '"+of_dest+"'")

            of_orig = os.path.join(path_orig, of_fmt%('y',of+i))
            of_dest = os.path.join(path_dest, of_fmt%('y',i+1))
            os.system("cp '"+of_orig+"' '"+of_dest+"'")

np.savetxt(index_path, index_list, fmt="%s")

missing_dir = []
incomplete_dir = []

#check missing and incomplete directories
for d in os.listdir(args.rgb_of_dir):
    path_dest = os.path.join(args.dest_dir, d+"/")

    if not os.path.isdir(path_dest): missing_dir.append(d)
    else:
        num_files = len(os.listdir(path_dest))
        if (num_files != 22): incomplete_dir.append(d)

np.savetxt(missing_path, missing_dir, fmt="%s")
np.savetxt(incomplete_path, incomplete_dir, fmt='%s')

