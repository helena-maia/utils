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

    yt_list = np.loadtxt(args.yt_id_list, delimiter=',',dtype=str)[1:] #ignore header
    
    in_fmt = os.path.join(args.video_dir,"%s_%s_%s.mp4") #(train_or_test, class, youtube_id)
    missing = []

    for v in yt_list:
        label, yt_id, split = v[[0,1,-1]]
        if not os.path.isfile(in_fmt%(split, label, yt_id)): 
            missing.append(v)

    np.savetxt(args.missing_list, missing, fmt="%s", delimiter=",")
