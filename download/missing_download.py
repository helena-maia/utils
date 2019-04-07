import os
import numpy as np
import argparse

def getArgs():
    parser = argparse.ArgumentParser(description='Download dataset.')
    parser.add_argument("yt_id_list", action='store', type=str, help="path to the list of youtube ids")
    parser.add_argument("video_dir", action='store', type=str, help="directory with the subclips")
    parser.add_argument("missing_list", action='store', type=str, help="path to the output")
    return parser.parse_args()



if __name__ == "__main__":
    args = getArgs()

    yt_list = np.loadtxt(args.yt_id_list, delimiter=',',dtype='U100')[1:] #ignore header
    
    in_fmt = os.path.join(args.video_dir,"%s_%s_%s_%04d.mp4") #(train_or_test, class, youtube_id, start_time)
    missing = []

    for i,v in enumerate(yt_list):
        print ("%d of %d"%(i,len(yt_list)))
        label, yt_id, split, start_time = v[0], v[1], v[-1], int(v[2])

        label = label.replace(" ","-")

        if(not label in in_fmt%(split, label, yt_id, start_time)):
           print (label, in_fmt%(split, label, yt_id, start_time))
           a = input()

        if not os.path.isfile(in_fmt%(split, label, yt_id, start_time)): 
            print (in_fmt%(split, label, yt_id, start_time))
            print (v)
            missing.append(v)

    np.savetxt(args.missing_list, missing, fmt="%s", delimiter=",")
