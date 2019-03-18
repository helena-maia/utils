import argparse
import os
import numpy as np
import cv2

def getArgs():
    parser = argparse.ArgumentParser(description='Estimate class predominant motion')
    parser.add_argument("rgb_of_dir", action='store', type=str, help="directory with rgb frames and optical images")
    parser.add_argument("class_ind", action='store', type=str, help="path to class_int.txt")
    parser.add_argument("direction_path",action='store', type=str, help="path to direction file")
    return parser.parse_args()

args = getArgs()

of_fmt = "flow_%c_%05d.jpg"

class_list = np.loadtxt(args.class_ind, delimiter=",", dtype=str)[:,0]
class_mov = np.zeros((len(class_list),2))

for d in os.listdir(args.rgb_of_dir):
    print (d)
    path_orig = os.path.join(args.rgb_of_dir, d+"/")

    total = int(len(os.listdir(path_orig))/3)
    diff_sum = 0

    if(total >= 10):
        for i in range(total):
            flow_x_path = os.path.join(path_orig, of_fmt%('x',i+1))
            flow_y_path = os.path.join(path_orig, of_fmt%('y',i+1))

            flow_x = cv2.imread(flow_x_path,0)
            flow_y = cv2.imread(flow_y_path,0)

            diff = flow_x - flow_y
            diff_sum+=diff.sum()

        class_name = d.split("_")[1]
        class_ind = np.argwhere(class_list == class_name).item()
        
        if(diff_sum >= 0): class_mov[class_ind][0]+=1
        else: class_mov[class_ind][1]+=1

direction = []

for name,mov in zip(class_list,class_mov):
    if (mov[0] > mov[1]): direction.append(name+",1")
    else: direction.append(name+",2")

np.savetxt(args.direction_path,direction,fmt="%s")